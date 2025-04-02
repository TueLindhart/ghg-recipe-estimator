import pytest

from food_co2_estimator.chains.rag_co2_estimator import NEGLIGIBLE_THRESHOLD
from food_co2_estimator.chains.search_co2_estimator import get_co2_search_emissions
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimate


@pytest.fixture
def enriched_recipe_for_search_test():
    return EnrichedRecipe(
        url="http://example.com",
        ingredients=[
            EnrichedIngredient(
                original_name="1 dåse salsa",
                en_name="1 can of salsa",
                weight_estimate=WeightEstimate(
                    ingredient="1 can of salsa",
                    weight_calculation="1 can = 400 g, 1 * 400 g = 400 g = 0.4 kg",
                    weight_in_kg=0.4,
                ),
            ),
            EnrichedIngredient(
                original_name="500 g vildtkød",
                en_name="500 g venison",
                weight_estimate=WeightEstimate(
                    ingredient="500 g venison",
                    weight_calculation="500 g = 500 g = 0.5 kg",
                    weight_in_kg=0.5,
                ),
            ),
            EnrichedIngredient(
                original_name="salt",
                en_name="salt",
                weight_estimate=WeightEstimate(
                    ingredient="salt",
                    weight_calculation="Amount of salt not specified. LLM estimate is: 1 serving = 0.005 kg, 2 servings * 0.005 kg = 0.01 kg",
                    weight_in_kg=0.01,
                ),
            ),
        ],
        persons=2,
        instructions="Bland ingredienserne",
    )


EXPECTED_RESULTS_RANGE = {"1 can of salsa": [1.0, 1.5], "500 g venison": [4, 6]}


@pytest.mark.asyncio
async def test_get_co2_search_emissions(
    enriched_recipe_for_search_test: EnrichedRecipe,
):
    # Call the function
    result = await get_co2_search_emissions(
        verbose=False,
        recipe=enriched_recipe_for_search_test,
        negligeble_threshold=NEGLIGIBLE_THRESHOLD,
    )

    # Assert the results
    assert len(result.search_results) == 2, "There should not be searched for salt."
    for search_result in result.search_results:
        assert search_result.unit == "kg CO2e per kg"
        assert search_result.result is not None
        lower, upper = EXPECTED_RESULTS_RANGE[search_result.ingredient]
        assert lower <= search_result.result <= upper
