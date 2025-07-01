import asyncio
import logging

from food_co2_estimator.blob_caching import cache_results
from food_co2_estimator.chains.rag_co2_estimator import (
    get_co2_emissions,
)
from food_co2_estimator.chains.recipe_extractor import extract_recipe
from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.language.detector import Languages
from food_co2_estimator.pydantic_models.estimator import RunParams
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from food_co2_estimator.pydantic_models.response_models import JobStatus
from food_co2_estimator.rediscache import RedisCache
from food_co2_estimator.url.url2markdown import get_markdown_from_url
from food_co2_estimator.utils.output_generator import (
    generate_output_model,
)


def log_exception_message(url: str, message: str):
    logging.exception(f"URL={url}: {message}")


@cache_results
async def async_estimator(
    runparams: RunParams,
    redis_client: RedisCache | None = None,
    logging_level: int = logging.INFO,
    verbose: bool = True,
    # Not ideal to pass redis client here, but for now
    # it is the only way to update status without major api changes
) -> tuple[bool, str]:
    logging.basicConfig(level=logging_level)
    await update_status(runparams.uid, redis_client, JobStatus.EXTRACTING_TEXT)
    text = get_markdown_from_url(runparams.url)
    if text is None:
        return False, "Kan ikke udtrække tekst fra URL"

    # Extract ingredients from text
    await update_status(runparams.uid, redis_client, JobStatus.EXTRACTING_RECIPE)
    recipe = await extract_recipe(text=text, url=runparams.url, verbose=verbose)
    if len(recipe.ingredients) == 0:
        no_recipe_message = "Kan ikke finde en opskrift for den angivne URL."
        log_exception_message(runparams.url, no_recipe_message)
        return False, no_recipe_message

    enriched_recipe = EnrichedRecipe.from_extracted_recipe(runparams.url, recipe)
    if enriched_recipe.language == Languages.Unknown:
        language_exception = f"Sproget blev ikke genkendt som et af følgende: {', '.join([lang.value for lang in Languages])}"
        log_exception_message(runparams.url, language_exception)
        return False, language_exception

    await update_status(runparams.uid, redis_client, JobStatus.ESTIMATING_WEIGHTS)
    try:
        # Estimate weights using weight estimator
        parsed_weight_output = await get_weight_estimates(
            verbose=verbose,
            recipe=enriched_recipe,
        )
        enriched_recipe.update_with_weight_estimates(parsed_weight_output)
    except Exception as e:
        weight_est_exception = "Noget gik galt under estimering af ingrediensers vægt."
        log_exception_message(runparams.url, str(e))
        log_exception_message(runparams.url, weight_est_exception)
        return False, weight_est_exception
    await update_status(runparams.uid, redis_client, JobStatus.ESTIMATING_CO2)
    try:
        # Estimate the kg CO2e per kg for each ingredient using RAG
        parsed_rag_emissions = await get_co2_emissions(
            verbose=verbose,
            negligeble_threshold=runparams.negligeble_threshold,
            recipe=enriched_recipe,
        )
        enriched_recipe.update_with_co2_per_kg_db(parsed_rag_emissions)
    except Exception as e:
        rag_emissions_exception = (
            "Noget gik galt under estimering af kg CO2e pr. kg for ingredienserne."
        )
        log_exception_message(runparams.url, str(e))
        log_exception_message(runparams.url, rag_emissions_exception)
        return False, rag_emissions_exception

    # Build a Pydantic model and return its JSON representation
    await update_status(runparams.uid, redis_client, JobStatus.PREPARING_OUTPUT)
    output_model = generate_output_model(
        enriched_recipe=enriched_recipe,
        negligeble_threshold=runparams.negligeble_threshold,
        number_of_persons=enriched_recipe.persons,
    )
    if (
        output_model.total_co2_kg == 0
        or output_model.co2_per_person_kg is None
        or output_model.co2_per_person_kg == 0
    ):
        calculation_failed_expection = "Udledningen blev nul, hvilket er forkert."
        return False, calculation_failed_expection

    return True, output_model.model_dump_json()


async def update_status(uid: str, redis_client: RedisCache | None, status: JobStatus):
    if redis_client is not None:
        await redis_client.update_job_status(uid=uid, status=status)


if __name__ == "__main__":
    from time import time

    # Example URLs (uncomment the one you want to test)
    # url = "https://www.foodfanatic.dk/tacos-med-lynchili-og-salsa"
    # url = "https://www.arla.dk/opskrifter/nytarstorsk-bagt-torsk-med-sennepssauce/"
    # url = "https://www.allrecipes.com/recipe/267703/dutch-oven-southwestern-chicken-pot-pie/"
    # url = "https://gourministeriet.dk/vores-favorit-bolognese/"
    # url = "https://hot-thai-kitchen.com/green-curry-new-2/"
    # url = "https://madogkaerlighed.dk/cremet-pasta-med-asparges/"
    url = "https://www.valdemarsro.dk/vegetar-enchiladas/"
    # url = "https://www.valdemarsro.dk/wok-med-kaal-og-friterede-spejlaeg/"
    # url = "https://www.louisesmadblog.dk/bloede-tacos/"

    start_time = time()
    runparams = RunParams(url=url)
    success, result = asyncio.run(
        async_estimator(
            runparams=runparams,
        )
    )
    print(result)
    end_time = time()
    print(f"Async time elapsed: {end_time - start_time}s")
