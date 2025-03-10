from langchain_core.runnables import RunnablePassthrough, RunnableSerializable

from food_co2_estimator.logger_utils import log_with_url
from food_co2_estimator.prompt_templates.rag_co2_estimator import (
    RAG_CO2_EMISSION_PROMPT,
)
from food_co2_estimator.pydantic_models.co2_estimator import CO2Emissions
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.retrievers.vector_db_retriever import batch_emission_retriever
from food_co2_estimator.utils.openai_model import get_model

NEGLIGIBLE_THRESHOLD = 0.025


def rag_co2_emission_chain(verbose: bool) -> RunnableSerializable:
    llm = get_model(
        pydantic_model=CO2Emissions,
        verbose=verbose,
    )

    return (
        {"context": batch_emission_retriever, "ingredients": RunnablePassthrough()}
        | RAG_CO2_EMISSION_PROMPT
        | llm
    )


def weight_above_negligeble_threshold(
    item: EnrichedIngredient, negligeble_threshold: float
) -> bool:
    return (
        item.weight_estimate is not None
        and item.weight_estimate.weight_in_kg is not None
        and item.weight_estimate.weight_in_kg > negligeble_threshold
    )


@log_with_url
async def get_co2_emissions(
    verbose: bool,
    negligeble_threshold: float,
    recipe: EnrichedRecipe,
) -> CO2Emissions:
    emission_chain = rag_co2_emission_chain(verbose)

    ingredients_input = [
        item.en_name
        for item in recipe.ingredients
        if weight_above_negligeble_threshold(item, negligeble_threshold)
    ]

    parsed_rag_emissions: CO2Emissions = await emission_chain.ainvoke(ingredients_input)

    return parsed_rag_emissions
