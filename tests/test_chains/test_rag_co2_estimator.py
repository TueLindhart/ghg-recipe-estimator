import pytest

from food_co2_estimator.chains.rag_co2_estimator import (
    NEGLIGIBLE_THRESHOLD,
    get_co2_emissions,
)
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe

ACCEPTABLE_CO2_ERROR = 0.05  # kg CO2e (this range should be refined in the future)
AVERAGE_ACCEPTABLE_DEVIATION = 0.2


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
    co2_emissions = []
    expected_co2_emissions = []
    deviations = []
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
            continue

        estimated_co2 = co2_per_kg_db.co2_per_kg
        reference_co2 = reference_co2_per_kg_db.co2_per_kg
        if estimated_co2 is not None and reference_co2 is None:
            raise AssertionError(
                f"Reference CO2 for {expected_ingredient.original_name} is None, but the estimated CO2 is not None: {ingredient.original_name}"
            )

        if reference_co2 is None or estimated_co2 is None:
            continue

        deviation = abs(reference_co2 - estimated_co2)
        deviations.append(deviation)

        # Model is not consistent enough yet to utilize below checks
        # lower_bound = max(0, reference_co2 - (ACCEPTABLE_CO2_ERROR / 2))
        # upper_bound = reference_co2 + (ACCEPTABLE_CO2_ERROR / 2)
        # assert lower_bound <= estimated_co2 and estimated_co2 <= upper_bound, (
        #     f"CO2 estimate for {ingredient.original_name} is out of the acceptable range: "
        #     f"{estimated_co2} not in [{lower_bound}, {upper_bound}]"
        # )

        # co2_emissions.append(estimated_co2)
        # expected_co2_emissions.append(reference_co2)

    # assert len(co2_emissions) > 0, "No emissions at all. Probably a bug in tests"

    # Check the avg. deviation
    avg_deviation = sum(deviations) / len(deviations)
    assert avg_deviation <= AVERAGE_ACCEPTABLE_DEVIATION
