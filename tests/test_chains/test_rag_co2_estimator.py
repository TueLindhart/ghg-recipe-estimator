import numpy as np
import pytest

from food_co2_estimator.chains.rag_co2_estimator import (
    NEGLIGIBLE_THRESHOLD,
    get_co2_emissions,
)
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)

ACCEPTABLE_RATIO_OF_DEVIATING_INGREDIENTS = 0.2  # 10 %
ACCEPTABLE_AVG_DEVIATION = 0.25  # kg


@pytest.mark.asyncio
async def test_rag_co2_estimator_chain(
    enriched_recipe_with_weight_est_fixture: tuple[str, EnrichedRecipe],
    enriched_recipe_with_co2_est_fixture: tuple[str, EnrichedRecipe],
):
    enriched_recipe = enriched_recipe_with_weight_est_fixture[1]
    expected_enriched_recipe = enriched_recipe_with_co2_est_fixture[1]

    assert not all(
        ingredient.weight_estimate is None
        for ingredient in expected_enriched_recipe.ingredients
    )

    rag_co2_emissions = await get_co2_emissions(
        verbose=False,
        recipe=enriched_recipe,
        negligeble_threshold=NEGLIGIBLE_THRESHOLD,
    )
    enriched_recipe.update_with_co2_per_kg_db(rag_co2_emissions)

    # Compare the CO2 emissions with the expected output
    deviations = []
    n_deviations = 0
    for ingredient, expected_ingredient in zip(
        enriched_recipe.ingredients, expected_enriched_recipe.ingredients
    ):
        assert (
            ingredient.original_name == expected_ingredient.original_name
        ), f"Ingredient mismatch: {ingredient.original_name} != {expected_ingredient.original_name}"

        co2_per_kg_db = ingredient.co2_per_kg_db
        reference_co2_per_kg_db = expected_ingredient.co2_per_kg_db
        if co2_per_kg_db is None and reference_co2_per_kg_db is not None:
            raise AssertionError(
                f"Estimated CO2 for {ingredient.original_name} is None, but the reference CO2 is not None: {expected_ingredient.original_name}"
            )

        if co2_per_kg_db is None or reference_co2_per_kg_db is None:
            deviations.append(0)
            continue

        assert co2_per_kg_db.unit in [
            "kg CO2e per kg",
            "kg CO2 per kg",
            "kg CO2e / kg",
            "kg CO2 / kg",
        ]

        estimated_co2 = co2_per_kg_db.co2_per_kg
        reference_co2 = reference_co2_per_kg_db.co2_per_kg
        if estimated_co2 is not None and reference_co2 is None:
            raise AssertionError(
                f"Reference CO2 for {expected_ingredient.original_name} is None, but the estimated CO2 is not None: {ingredient.original_name}"
            )

        if reference_co2 is None or estimated_co2 is None:
            deviations.append(0)
            continue

        deviation = abs(reference_co2 - estimated_co2)
        deviations.append(deviation)

        if deviation != 0:
            n_deviations += 1

    # Check the avg. deviation
    avg_deviation = sum(deviations) / len(deviations)
    error_message = f"kg CO2 / kg est. varies in avg. on: {round(avg_deviation, 2)} kg"
    error_message += f"\n{print_max_deviation_ingredient(enriched_recipe.ingredients,
                                                         expected_enriched_recipe.ingredients,
                                                         deviations,)}"
    assert avg_deviation <= ACCEPTABLE_AVG_DEVIATION, error_message

    ratio_of_deviating_ingredients = n_deviations / len(deviations)
    assert (
        ratio_of_deviating_ingredients < ACCEPTABLE_RATIO_OF_DEVIATING_INGREDIENTS
    ), f"{round(ratio_of_deviating_ingredients * 100, 2)}% of ingredients varies in kg CO2 per kg results"


def print_max_deviation_ingredient(
    ingredients: list[EnrichedIngredient],
    expected_ingredients: list[EnrichedIngredient],
    deviations: list[float],
) -> str:
    max_deviation = np.max(deviations)
    max_index = np.argmax(deviations)
    ingredient = ingredients[max_index]
    expected_ingredient = expected_ingredients[max_index]

    estimated_co2: float = ingredient.co2_per_kg_db.co2_per_kg  # type: ignore
    reference_co2: float = expected_ingredient.co2_per_kg_db.co2_per_kg  # type: ignore

    return f"""Ingredient with maximum deviation: {ingredient.original_name}\n
            Estimated CO2: {estimated_co2} kg CO2 / kg\n"
            Reference CO2: {reference_co2} kg CO2 / kg\n"
            Deviation: {max_deviation} kg CO2 / kg
            """
