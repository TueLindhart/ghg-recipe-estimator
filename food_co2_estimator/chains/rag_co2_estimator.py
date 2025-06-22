from functools import partial

from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableSerializable,
)

from food_co2_estimator.language.detector import Languages
from food_co2_estimator.logger_utils import log_with_url
from food_co2_estimator.prompt_templates.rag_co2_estimator import (
    RAG_CO2_EMISSION_PROMPT,
)
from food_co2_estimator.pydantic_models.co2_estimator import CO2Emissions
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.retrievers.vector_db_retriever import (
    batch_emission_retriever,
    clean_ingredient,
)
from food_co2_estimator.utils.llm_model import LLMFactory

NEGLIGIBLE_THRESHOLD = 0.005  # Remove threshold?
INGREDIENTS_TO_IGNORE = ["salt", "water", "pepper"]


def rag_co2_emission_chain(verbose: bool, language: Languages) -> RunnableSerializable:
    llm = LLMFactory(
        output_model=CO2Emissions,
        verbose=verbose,
    ).get_model()

    # ---- Context retriever --------------------------------------------------
    # RunnableLambda takes the single chain input (the question) and expands
    # it into the (question, language) call expected by `batch_emission_retriever`.
    context_runnable = RunnableLambda(
        partial(batch_emission_retriever, language=language)
    )

    # ---- Chain --------------------------------------------------------------
    return (
        {
            "context": context_runnable,  # <- uses (question, language)
            "ingredients": RunnablePassthrough(),  # forwards the raw question
        }
        | RAG_CO2_EMISSION_PROMPT
        | llm
    )


def should_include_ingredient(
    item: EnrichedIngredient, negligeble_threshold: float
) -> bool:
    return above_weight_threshold(item, negligeble_threshold) and ingredient_to_ignore(
        item
    )


def above_weight_threshold(
    item: EnrichedIngredient, negligeble_threshold: float
) -> bool:
    return (
        item.weight_estimate is not None
        and item.weight_estimate.weight_in_kg is not None
        and negligeble_threshold < item.weight_estimate.weight_in_kg
    )


def ingredient_to_ignore(item: EnrichedIngredient) -> bool:
    if item.name is None:
        return True
    ingredient = clean_ingredient(item.name)
    return not any(
        ignored_ingredient == ingredient for ignored_ingredient in INGREDIENTS_TO_IGNORE
    )


@log_with_url
async def get_co2_emissions(
    *,
    verbose: bool,
    negligeble_threshold: float,
    recipe: EnrichedRecipe,
) -> CO2Emissions:
    emission_chain = rag_co2_emission_chain(verbose, recipe.language)

    ingredients_input = [
        item.name
        for item in recipe.ingredients
        if should_include_ingredient(item, negligeble_threshold)
    ]

    parsed_rag_emissions: CO2Emissions = await emission_chain.ainvoke(ingredients_input)

    return parsed_rag_emissions
