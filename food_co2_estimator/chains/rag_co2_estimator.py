from functools import lru_cache, partial
from pathlib import Path

import pandas as pd  # pyright: ignore[reportMissingImports]
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
from food_co2_estimator.pydantic_models.co2_estimator import (
    CO2Emissions,
    CO2Matches,
    CO2perKg,
)
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
FOODDATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "fooddatabase.xlsx"
)


@lru_cache(maxsize=1)
def _load_emission_data() -> dict[str, dict[str, str]]:
    """Load emission metadata from the DBv2.xlsx DK sheet using pandas."""
    df = pd.read_excel(FOODDATABASE_PATH, sheet_name="DK")
    data: dict[str, dict[str, str]] = {}
    for record in df.to_dict(orient="records"):
        key = record.get("ID_Ra")
        if key is not None and key != "":
            data[str(key)] = {
                str(k): str(v) if v is not None else "" for k, v in record.items()
            }
    return data


def _enrich_matches(matches: CO2Matches) -> CO2Emissions:
    data = _load_emission_data()
    enriched: list[CO2perKg] = []

    def safe_float(row: dict[str, str], key: str) -> float | None:
        value = row.get(key)
        if value in (None, ""):
            return None
        try:
            return float(value)
        except ValueError:
            return None

    for match in matches.emissions:
        row = data.get(match.ingredient_id, {})
        enriched.append(
            CO2perKg(
                closest_match_explanation=match.closest_match_explanation,
                ingredient_id=match.ingredient_id,
                closest_match_name=match.closest_match_name,
                ingredient=match.ingredient,
                unit=match.unit,
                co2_per_kg=match.co2_per_kg,
                energy_kj_100g=safe_float(row, "Energi (KJ/100 g)"),
                fat_g_100g=safe_float(row, "Fedt (g/100 g)"),
                carbohydrate_g_100g=safe_float(row, "Kulhydrat (g/100 g)"),
                protein_g_100g=safe_float(row, "Protein (g/100 g)"),
            )
        )

    return CO2Emissions(emissions=enriched)


def rag_co2_emission_chain(verbose: bool, language: Languages) -> RunnableSerializable:
    llm = LLMFactory(
        output_model=CO2Matches,
        verbose=verbose,
    ).get_model()

    context_runnable = RunnableLambda(
        partial(batch_emission_retriever, language=language)
    )

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

    parsed_rag_emissions: CO2Matches = await emission_chain.ainvoke(ingredients_input)

    return _enrich_matches(parsed_rag_emissions)
