import pytest

from food_co2_estimator.language.detector import Languages
from food_co2_estimator.pydantic_models.co2_estimator import CO2perKg
from food_co2_estimator.pydantic_models.estimator import (
    IngredientOutput,
    RecipeCO2Output,
)
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimate
from food_co2_estimator.utils.output_generator import (
    generate_output_model,
)


@pytest.fixture
def enriched_recipe_db_english():
    return EnrichedRecipe(
        title="Test Recipe",
        language=Languages.English,
        ingredients=[
            EnrichedIngredient(
                name="2 tomatoes",
                weight_estimate=WeightEstimate(
                    ingredient="2 tomatoes",
                    weight_calculation="2 tomatoes = 200g",
                    weight_in_kg=0.2,
                ),
                co2_per_kg_db=CO2perKg(
                    closest_match_explanation="Database entry",
                    closest_match_name="tomatoes, canned",
                    ingredient_id="123",
                    ingredient="2 tomatoes",
                    co2_per_kg=2.5,
                    unit="kg CO₂e / kg",
                    energy_kj_100g=90.0,
                    fat_g_100g=0.2,
                    carbohydrate_g_100g=3.0,
                    protein_g_100g=1.0,
                ),
            ),
            EnrichedIngredient(
                name="1 liter of milk",
                weight_estimate=WeightEstimate(
                    ingredient="1 liter of milk",
                    weight_calculation="1 liter = 1kg",
                    weight_in_kg=1.0,
                ),
                co2_per_kg_db=CO2perKg(
                    closest_match_explanation="Database entry",
                    ingredient="1 liter of milk",
                    ingredient_id="456",
                    closest_match_name="milk",
                    co2_per_kg=1.0,
                    unit="kg CO₂e / kg",
                    energy_kj_100g=250.0,
                    fat_g_100g=3.0,
                    carbohydrate_g_100g=5.0,
                    protein_g_100g=3.0,
                ),
            ),
            EnrichedIngredient(
                name="3 large eggs",
                weight_estimate=WeightEstimate(
                    ingredient="3 large eggs",
                    weight_calculation="3 large eggs = 150g",
                    weight_in_kg=0.15,
                ),
                co2_per_kg_db=CO2perKg(
                    closest_match_explanation="Database entry",
                    closest_match_name="eggs",
                    ingredient="3 large eggs",
                    ingredient_id="789",
                    co2_per_kg=3.0,
                    unit="kg CO₂e / kg",
                    energy_kj_100g=600.0,
                    fat_g_100g=10.0,
                    carbohydrate_g_100g=1.0,
                    protein_g_100g=12.0,
                ),
            ),
        ],
        persons=4,
        instructions="Mix ingredients",
        url="http://example.com",
    )


@pytest.mark.parametrize(
    "enriched_recipe, negligeble_threshold, expected_output",
    [
        (
            "enriched_recipe_db_english",
            0.1,
            RecipeCO2Output(
                title="Test Recipe",
                url="http://example.com",
                total_co2_kg=1.9,
                number_of_persons=4,
                co2_per_person_kg=0.5,
                total_energy_kj=3580.0,
                total_fat_g=45.4,
                total_carbohydrate_g=57.5,
                total_protein_g=50.0,
                avg_meal_emission_per_person_range_kg=[1.3, 2.2],
                ingredients=[
                    IngredientOutput(
                        name="1 liter of milk",
                        ingredient_id="456",
                        weight_kg=1.0,
                        co2_per_kg=1.0,
                        co2_kg=1.0,
                        calculation_notes="1.0 kg * 1.0 kg CO₂e/kg = 1.0 kg CO₂e",
                        weight_estimation_notes="1 liter = 1kg",
                        co2_emission_notes="Bedste match i CO₂-databasen er: milk",
                        energy_kj=2500.0,
                        fat_g=30.0,
                        carbohydrate_g=50.0,
                        protein_g=30.0,
                    ),
                    IngredientOutput(
                        name="2 tomatoes",
                        ingredient_id="123",
                        weight_kg=0.2,
                        co2_per_kg=2.5,
                        co2_kg=0.5,
                        calculation_notes="0.2 kg * 2.5 kg CO₂e/kg = 0.5 kg CO₂e",
                        weight_estimation_notes="2 tomatoes = 200g",
                        co2_emission_notes="Bedste match i CO₂-databasen er: tomatoes, canned",
                        energy_kj=180.0,
                        fat_g=0.4,
                        carbohydrate_g=6.0,
                        protein_g=2.0,
                    ),
                    IngredientOutput(
                        name="3 large eggs",
                        ingredient_id="789",
                        weight_kg=0.15,
                        co2_per_kg=3.0,
                        co2_kg=0.45,
                        calculation_notes="0.15 kg * 3.0 kg CO₂e/kg = 0.45 kg CO₂e",
                        weight_estimation_notes="3 large eggs = 150g",
                        co2_emission_notes="Bedste match i CO₂-databasen er: eggs",
                        energy_kj=900.0,
                        fat_g=15.0,
                        carbohydrate_g=1.5,
                        protein_g=18.0,
                    ),
                ],
            ),
        ),
    ],
    ids=[
        "test_db_english",
    ],
)
def test_generate_output(
    request: pytest.FixtureRequest,
    enriched_recipe: str,
    negligeble_threshold: float,
    expected_output: RecipeCO2Output,
) -> None:
    recipe = request.getfixturevalue(enriched_recipe)
    result = generate_output_model(
        enriched_recipe=recipe,
        negligeble_threshold=negligeble_threshold,
        number_of_persons=4,
    )
    assert result.model_dump() == expected_output.model_dump()
