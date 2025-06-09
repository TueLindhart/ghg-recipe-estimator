import re

import pytest

from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from food_co2_estimator.pydantic_models.weight_estimator import (
    WeightEstimate,
    WeightEstimates,
)

ACCEPTABLE_WEIGHT_ERROR = 0.2  # +/- 0.2 kg
TOTAL_ACCEPTABLE_RATIO_ERROR = 0.075  # +/- 7.5% of total weight
IN_KG_REGEX = r"= \d+(\.\d+)? (kg|kilogram)"


def validate_ingredient_names(
    ingredient: WeightEstimate, expected: WeightEstimate
) -> None:
    """Validate that ingredient names match."""
    assert (
        ingredient.ingredient.strip() == expected.ingredient.strip()
    ), f"Ingredient mismatch: {ingredient.ingredient} != {expected.ingredient}"


def validate_weight_exists(
    ingredient: WeightEstimate, expected: WeightEstimate
) -> None:
    """Validate that weight exists if it should."""
    if ingredient.weight_in_kg is None and expected.weight_in_kg is not None:
        raise AssertionError(
            f"Estimated weight for {ingredient.ingredient} is None, "
            f"but reference weight is not None: {expected.weight_in_kg}"
        )


def validate_weight_bounds(
    ingredient: WeightEstimate, expected: WeightEstimate
) -> None:
    """Validate that weight is within acceptable bounds."""
    if expected.weight_in_kg is not None and ingredient.weight_in_kg is not None:
        lower_bound = max(0, expected.weight_in_kg - ACCEPTABLE_WEIGHT_ERROR)
        upper_bound = expected.weight_in_kg + ACCEPTABLE_WEIGHT_ERROR
        assert lower_bound <= ingredient.weight_in_kg <= upper_bound, (
            f"Weight estimate for {ingredient.ingredient} is out of range: "
            f"{ingredient.weight_in_kg} not in [{lower_bound}, {upper_bound}]"
        )


def validate_weight_calculation(
    ingredient: WeightEstimate, expected: WeightEstimate
) -> None:
    """Validate that weight calculation is in kg and matches expected."""
    if (
        not re.search(IN_KG_REGEX, ingredient.weight_calculation)
        and ingredient.weight_calculation != expected.weight_calculation
    ):
        raise AssertionError(
            f"Weight calculation for {ingredient.ingredient} not in kg: "
            f"{ingredient.weight_calculation}"
        )


def validate_ingredient_weights(
    ingredient: WeightEstimate, expected: WeightEstimate
) -> None:
    """Run all weight validations for a single ingredient pair."""
    validate_ingredient_names(ingredient, expected)
    validate_weight_exists(ingredient, expected)
    validate_weight_bounds(ingredient, expected)
    validate_weight_calculation(ingredient, expected)


def calculate_total_weight(weight_estimates: WeightEstimates) -> float:
    """Calculate total weight from weight estimates."""
    return sum(
        ing.weight_in_kg
        for ing in weight_estimates.weight_estimates
        if ing.weight_in_kg is not None
    )


def calculate_ratio_differences(
    weight_estimates: WeightEstimates,
    expected_weight_estimates: WeightEstimates,
) -> tuple[float, list[tuple[str, float]]]:
    """Calculate total ratio difference and per-ingredient differences."""
    # Calculate total weights
    estimated_total = calculate_total_weight(weight_estimates)
    reference_total = calculate_total_weight(expected_weight_estimates)

    total_ratio_diff = abs(estimated_total - reference_total) / reference_total

    # Calculate per-ingredient differences
    differences = []
    for ing, exp_ing in zip(
        weight_estimates.weight_estimates, expected_weight_estimates.weight_estimates
    ):
        if ing.weight_in_kg and exp_ing.weight_in_kg:
            ratio = abs(ing.weight_in_kg - exp_ing.weight_in_kg) / exp_ing.weight_in_kg
            differences.append((ing.ingredient, ratio))

    return total_ratio_diff, differences


@pytest.mark.asyncio
async def test_weight_estimator_chain(
    enriched_recipe_with_weight_est_fixture: tuple[str, EnrichedRecipe],
):
    enriched_recipe = enriched_recipe_with_weight_est_fixture[1]
    expected_weight_estimates = WeightEstimates(
        weight_estimates=[
            ingredient.weight_estimate
            for ingredient in enriched_recipe.ingredients
            if ingredient.weight_estimate is not None
        ]
    )

    weight_estimates = await get_weight_estimates(verbose=False, recipe=enriched_recipe)

    # Validate individual ingredients
    for ingredient, expected in zip(
        weight_estimates.weight_estimates, expected_weight_estimates.weight_estimates
    ):
        validate_ingredient_weights(ingredient, expected)

    # Calculate and validate total ratio differences
    ratio_difference, ingredient_differences = calculate_ratio_differences(
        weight_estimates, expected_weight_estimates
    )

    assert ratio_difference <= TOTAL_ACCEPTABLE_RATIO_ERROR, (
        f"Total weight estimate is out of acceptable range: "
        f"ratio_difference={ratio_difference:.3f}, "
        f"per_ingredient_differences={ingredient_differences} "
        f"(threshold={TOTAL_ACCEPTABLE_RATIO_ERROR})"
    )
