import asyncio
import logging

from food_co2_estimator.blob_caching import cache_results
from food_co2_estimator.chains.rag_co2_estimator import (
    get_co2_emissions,
)
from food_co2_estimator.chains.recipe_extractor import extract_recipe
from food_co2_estimator.chains.search_co2_estimator import get_co2_search_emissions
from food_co2_estimator.chains.translator import get_translation_chain
from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.language.detector import Languages, detect_language
from food_co2_estimator.pydantic_models.estimator import LogParams, RunParams
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from food_co2_estimator.url.url2markdown import get_markdown_from_url
from food_co2_estimator.utils.output_generator import (
    generate_output_model,
)


def log_exception_message(url: str, message: str):
    logging.exception(f"URL={url}: {message}")


@cache_results
async def async_estimator(
    runparams: RunParams,
    logparams: LogParams | None = None,
) -> tuple[bool, str]:
    if logparams is None:
        logparams = LogParams()
    logging.basicConfig(level=logparams.logging_level)
    text = get_markdown_from_url(runparams.url)
    if text is None:
        return False, "Unable to extract text from provided URL"

    # Extract ingredients from text
    recipe = await extract_recipe(
        text=text, url=runparams.url, verbose=logparams.verbose
    )
    if len(recipe.ingredients) == 0:
        no_recipe_message = "I can't find a recipe in the provided URL."
        log_exception_message(runparams.url, no_recipe_message)
        return False, no_recipe_message

    # Detect language in ingredients
    enriched_recipe = EnrichedRecipe.from_extracted_recipe(runparams.url, recipe)
    language = detect_language(enriched_recipe)
    if language is None:
        language_exception = f"Language is not recognized as {', '.join([lang.value for lang in Languages])}"
        log_exception_message(runparams.url, language_exception)
        return False, language_exception

    translator = get_translation_chain()
    try:
        enriched_recipe: EnrichedRecipe = await translator.ainvoke(
            {"recipe": enriched_recipe, "language": language}
        )
    except Exception as e:
        translation_exception = "Something went wrong in translating recipes."
        log_exception_message(runparams.url, str(e))
        log_exception_message(runparams.url, translation_exception)
        return False, translation_exception

    try:
        # Estimate weights using weight estimator
        parsed_weight_output = await get_weight_estimates(
            logparams.verbose, enriched_recipe
        )
        enriched_recipe.update_with_weight_estimates(parsed_weight_output)
    except Exception as e:
        weight_est_exception = (
            "Something went wrong in estimating weights of ingredients."
        )
        log_exception_message(runparams.url, str(e))
        log_exception_message(runparams.url, weight_est_exception)
        return False, weight_est_exception

    try:
        # Estimate the kg CO2e per kg for each ingredient using RAG
        parsed_rag_emissions = await get_co2_emissions(
            logparams.verbose, runparams.negligeble_threshold, enriched_recipe
        )
        enriched_recipe.update_with_co2_per_kg_db(parsed_rag_emissions)
    except Exception as e:
        rag_emissions_exception = (
            "Something went wrong in estimating kg CO2e per kg for the ingredients."
        )
        log_exception_message(runparams.url, str(e))
        log_exception_message(runparams.url, rag_emissions_exception)
        return False, rag_emissions_exception

    # Check if any ingredients need a CO2 search estimation
    try:
        parsed_search_results = await get_co2_search_emissions(
            logparams.verbose, enriched_recipe, runparams.negligeble_threshold
        )
        enriched_recipe.update_with_co2_per_kg_search(parsed_search_results)
    except Exception as e:
        search_emissions_exception = (
            "Something went wrong when searching for kg CO2e per kg."
        )
        log_exception_message(runparams.url, str(e))
        log_exception_message(runparams.url, search_emissions_exception)

    # Build a Pydantic model and return its JSON representation
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
        calculation_failed_expection = "Emission became zero which is incorrect."
        return False, calculation_failed_expection

    return True, output_model.model_dump_json()


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
