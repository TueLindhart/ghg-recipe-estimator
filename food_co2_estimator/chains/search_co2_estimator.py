from langchain_core.runnables import RunnablePassthrough

from food_co2_estimator.chains.rag_co2_estimator import (
    weight_above_negligeble_threshold,
)
from food_co2_estimator.logging_wrapper import log_with_url
from food_co2_estimator.prompt_templates.search_co2_estimator import (
    SEARCH_CO2_EMISSION_PROMPT,
)
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.pydantic_models.search_co2_estimator import CO2SearchResults
from food_co2_estimator.retrievers.search_retriever import batch_co2_search_retriever
from food_co2_estimator.utils.openai_model import get_model


def get_search_co2_emission_chain(verbose: bool):
    llm = get_model(
        pydantic_model=CO2SearchResults,
        verbose=verbose,
    )

    return (
        {
            "search_results": batch_co2_search_retriever,
            "ingredients": RunnablePassthrough(),
        }
        | SEARCH_CO2_EMISSION_PROMPT
        | llm
    )


def co2_per_kg_not_found(item: EnrichedIngredient):
    return item.co2_per_kg_db is None or item.co2_per_kg_db.co2_per_kg is None


@log_with_url
async def get_co2_search_emissions(
    verbose: bool,
    recipe: EnrichedRecipe,
    negligeble_threshold: float,
) -> CO2SearchResults:
    co2_search_input_items = [
        item.en_name
        for item in recipe.ingredients
        if co2_per_kg_not_found(item)
        and weight_above_negligeble_threshold(item, negligeble_threshold)
        and item.en_name is not None
    ]
    if not co2_search_input_items:
        return CO2SearchResults(search_results=[])
    search_chain = get_search_co2_emission_chain(verbose=verbose)
    search_results: CO2SearchResults = await search_chain.ainvoke(
        co2_search_input_items
    )  # type: ignore
    return search_results
