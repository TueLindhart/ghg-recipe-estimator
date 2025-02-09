import asyncio
import logging

from food_co2_estimator.chains.rag_co2_estimator import (
    NEGLIGIBLE_THRESHOLD,
    get_co2_emissions,
)
from food_co2_estimator.chains.recipe_extractor import extract_recipe
from food_co2_estimator.chains.search_co2_estimator import get_co2_search_emissions
from food_co2_estimator.chains.translator import get_translation_chain
from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.language.detector import Languages, detect_language
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from food_co2_estimator.url.url2markdown import get_markdown_from_url
from food_co2_estimator.utils.output_generator import (
    generate_output_model,  # This function returns a Pydantic model
)


def log_exception_message(url: str, message: str):
    logging.exception(f"URL={url}: {message}")


async def async_estimator(
    url: str,
    verbose: bool = False,
    negligeble_threshold: float = NEGLIGIBLE_THRESHOLD,
    logging_level=logging.INFO,
) -> str:
    logging.basicConfig(level=logging_level)
    text = get_markdown_from_url(url)
    if text is None:
        return "Unable to extract text from provided URL"

    # Extract ingredients from text
    recipe = await extract_recipe(text=text, url=url, verbose=verbose)
    if len(recipe.ingredients) == 0:
        no_recipe_message = "I can't find a recipe in the provided URL."
        log_exception_message(url, no_recipe_message)
        return no_recipe_message

    # Detect language in ingredients
    enriched_recipe = EnrichedRecipe.from_extracted_recipe(url, recipe)
    language = detect_language(enriched_recipe)
    if language is None:
        language_exception = f"Language is not recognized as {', '.join([lang.value for lang in Languages])}"
        log_exception_message(url, language_exception)
        return language_exception

    translator = get_translation_chain()
    try:
        enriched_recipe: EnrichedRecipe = await translator.ainvoke(
            {"recipe": enriched_recipe, "language": language}
        )
    except Exception as e:
        translation_exception = "Something went wrong in translating recipes."
        log_exception_message(url, str(e))
        log_exception_message(url, translation_exception)
        return translation_exception

    try:
        # Estimate weights using weight estimator
        parsed_weight_output = await get_weight_estimates(verbose, enriched_recipe)
        enriched_recipe.update_with_weight_estimates(parsed_weight_output)
    except Exception as e:
        weight_est_exception = (
            "Something went wrong in estimating weights of ingredients."
        )
        log_exception_message(url, str(e))
        log_exception_message(url, weight_est_exception)
        return weight_est_exception

    try:
        # Estimate the kg CO2e per kg for each ingredient using RAG
        parsed_rag_emissions = await get_co2_emissions(
            verbose, negligeble_threshold, enriched_recipe
        )
        enriched_recipe.update_with_co2_per_kg_db(parsed_rag_emissions)
    except Exception as e:
        rag_emissions_exception = (
            "Something went wrong in estimating kg CO2e per kg for the ingredients."
        )
        log_exception_message(url, str(e))
        log_exception_message(url, rag_emissions_exception)
        return rag_emissions_exception

    # Check if any ingredients need a CO2 search estimation
    try:
        parsed_search_results = await get_co2_search_emissions(
            verbose, enriched_recipe, negligeble_threshold
        )
        enriched_recipe.update_with_co2_per_kg_search(parsed_search_results)
    except Exception as e:
        search_emissions_exception = (
            "Something went wrong when searching for kg CO2e per kg."
        )
        log_exception_message(url, str(e))
        log_exception_message(url, search_emissions_exception)

    # Build a Pydantic model and return its JSON representation
    output_model = generate_output_model(
        enriched_recipe=enriched_recipe,
        negligeble_threshold=negligeble_threshold,
        number_of_persons=enriched_recipe.persons,
    )
    return output_model.model_dump_json()


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
    result = asyncio.run(
        async_estimator(
            url=url, verbose=True, logging_level=logging.INFO, return_output_string=True
        )
    )
    print(result)
    end_time = time()
    print(f"Async time elapsed: {end_time - start_time}s")
