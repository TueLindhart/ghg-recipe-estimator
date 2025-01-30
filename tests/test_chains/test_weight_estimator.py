import re

import pytest

from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimates

ACCEPTABLE_WEIGHT_ERROR = 0.2  # kg (this range should be refined in the future)
TOTAL_ACCEPTABLE_ERROR = 0.1

IN_KG_REGEX = r"= \d+(\.\d+)? (kg|kilogram)"


@pytest.mark.asyncio
async def test_weight_estimator_chain(
    enriched_recipe_with_weight_est_fixture: tuple[str, EnrichedRecipe],
):
    enriched_recipe = enriched_recipe_with_weight_est_fixture[1]
    # Parse the expected weight estimates
    expected_weight_estimates = WeightEstimates(
        weight_estimates=[
            ingredient.weight_estimate
            for ingredient in enriched_recipe.ingredients
            if ingredient.weight_estimate is not None
        ]
    )

    # Estimate weights using weight estimator
    weight_estimates = await get_weight_estimates(verbose=False, recipe=enriched_recipe)

    # Compare the weight estimates with the expected output
    for ingredient, expected_ingredient in zip(
        weight_estimates.weight_estimates, expected_weight_estimates.weight_estimates
    ):
        assert (
            ingredient.ingredient == expected_ingredient.ingredient
        ), f"Ingredient mismatch: {ingredient.ingredient} != {expected_ingredient.ingredient}"
        estimated_weight = ingredient.weight_in_kg
        reference_weight = expected_ingredient.weight_in_kg
        if estimated_weight is None and reference_weight is not None:
            raise AssertionError(
                f"Estimated weight for {ingredient.ingredient} is None, but the reference weight is not None: {reference_weight}"
            )

        if reference_weight is not None and estimated_weight is not None:
            lower_bound = max(0, reference_weight - ACCEPTABLE_WEIGHT_ERROR)
            upper_bound = reference_weight + ACCEPTABLE_WEIGHT_ERROR
            assert (
                lower_bound <= estimated_weight and estimated_weight <= upper_bound
            ), (
                f"Weight estimate for {ingredient.ingredient} is out of the acceptable range: "
                f"{estimated_weight} not in [{lower_bound}, {upper_bound}]"
            )

            weight_calculation = ingredient.weight_calculation
            expected_weight_calculation = expected_ingredient.weight_calculation
            if (
                not re.search(IN_KG_REGEX, weight_calculation)
                and weight_calculation != expected_weight_calculation
            ):
                raise AssertionError(
                    f"Weight calculation for {ingredient.ingredient} is not in kg: {weight_calculation}"
                )

    # Check the total weight
    estimated_total_weight = sum(
        ingredient.weight_in_kg
        for ingredient in weight_estimates.weight_estimates
        if ingredient.weight_in_kg is not None
    )
    reference_total_weight = sum(
        ingredient.weight_in_kg
        for ingredient in expected_weight_estimates.weight_estimates
        if ingredient.weight_in_kg is not None
    )
    lower_bound = max(0, reference_total_weight - TOTAL_ACCEPTABLE_ERROR)
    upper_bound = reference_total_weight + TOTAL_ACCEPTABLE_ERROR
    assert (
        lower_bound <= estimated_total_weight and estimated_total_weight <= upper_bound
    ), (
        f"Total weight estimate is out of the acceptable range: "
        f"{estimated_total_weight} not in [{lower_bound}, {upper_bound}]"
    )
