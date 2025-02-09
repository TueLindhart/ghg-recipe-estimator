import pytest

from food_co2_estimator.pydantic_models.co2_estimator import CO2perKg
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.pydantic_models.search_co2_estimator import CO2SearchResult
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimate
from food_co2_estimator.utils.output_generator import (
    IngredientOutput,
    RecipeCO2Output,
    generate_output_model,
)


@pytest.fixture
def enriched_recipe_db_english():
    return EnrichedRecipe(
        url="http://example.com",
        ingredients=[
            EnrichedIngredient(
                original_name="2 tomatoes",
                en_name="2 tomatoes",
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
                    unit="kg CO2e / kg",
                ),
            ),
            EnrichedIngredient(
                original_name="1 liter of milk",
                en_name="1 liter of milk",
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
                    unit="kg CO2e / kg",
                ),
            ),
            EnrichedIngredient(
                original_name="3 large eggs",
                en_name="3 large eggs",
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
                    unit="kg CO2e / kg",
                ),
            ),
        ],
        persons=4,
        instructions="Mix ingredients",
    )


@pytest.fixture
def enriched_recipe_search_english():
    return EnrichedRecipe(
        url="http://example.com",
        ingredients=[
            EnrichedIngredient(
                original_name="2 tomatoes",
                en_name="2 tomatoes",
                weight_estimate=WeightEstimate(
                    ingredient="2 tomatoes",
                    weight_calculation="2 tomatoes = 200g",
                    weight_in_kg=0.2,
                ),
                co2_per_kg_search=CO2SearchResult(
                    ingredient="2 tomatoes",
                    result=2.0,
                    explanation="Search result",
                    unit="kg CO2e / kg",
                ),
            ),
            EnrichedIngredient(
                original_name="1 liter of milk",
                en_name="1 liter of milk",
                weight_estimate=WeightEstimate(
                    ingredient="1 liter of milk",
                    weight_calculation="1 liter = 1kg",
                    weight_in_kg=1.0,
                ),
                co2_per_kg_search=CO2SearchResult(
                    ingredient="1 liter of milk",
                    result=1.0,
                    explanation="Search result",
                    unit="kg CO2e / kg",
                ),
            ),
            EnrichedIngredient(
                original_name="3 large eggs",
                en_name="3 large eggs",
                weight_estimate=WeightEstimate(
                    ingredient="3 large eggs",
                    weight_calculation="3 large eggs = 150g",
                    weight_in_kg=0.15,
                ),
                co2_per_kg_search=CO2SearchResult(
                    ingredient="3 large eggs",
                    result=3.0,
                    explanation="Search result",
                    unit="kg CO2e / kg",
                ),
            ),
        ],
        persons=4,
        instructions="Mix ingredients",
    )


# @pytest.fixture
# def enriched_recipe_db_danish():
#     return EnrichedRecipe(
#         url="http://example.com",
#         ingredients=[
#             EnrichedIngredient(
#                 original_name="2 tomater",
#                 en_name="2 tomatoes",
#                 weight_estimate=WeightEstimate(
#                     ingredient="2 tomatoes",
#                     weight_calculation="2 tomatoes = 200g",
#                     weight_in_kg=0.2,
#                 ),
#                 co2_per_kg_db=CO2perKg(
#                     ingredient="2 tomatoes",
#                     ingredient_id="123",
#                     co2_per_kg=2.5,
#                     closest_match_explanation="Database entry",
#                     closest_match_name="tomatoes, canned",
#                     unit="kg CO2e / kg",
#                 ),
#             ),
#             EnrichedIngredient(
#                 original_name="1 liter mælk",
#                 en_name="1 liter of milk",
#                 weight_estimate=WeightEstimate(
#                     ingredient="1 liter of milk",
#                     weight_calculation="1 liter = 1kg",
#                     weight_in_kg=1.0,
#                 ),
#                 co2_per_kg_db=CO2perKg(
#                     ingredient="1 liter of milk",
#                     ingredient_id="456",
#                     co2_per_kg=1.0,
#                     closest_match_explanation="Database entry",
#                     closest_match_name="tomatoes, canned",
#                     unit="kg CO2e / kg",
#                 ),
#             ),
#             EnrichedIngredient(
#                 original_name="3 store æg",
#                 en_name="3 large eggs",
#                 weight_estimate=WeightEstimate(
#                     ingredient="3 large eggs",
#                     weight_calculation="3 large eggs = 150g",
#                     weight_in_kg=0.15,
#                 ),
#                 co2_per_kg_db=CO2perKg(
#                     ingredient="3 large eggs",
#                     ingredient_id="789",
#                     co2_per_kg=3.0,
#                     closest_match_explanation="Database entry",
#                     closest_match_name="tomatoes, canned",
#                     unit="kg CO2e / kg",
#                 ),
#             ),
#         ],
#         persons=4,
#         instructions="Mix ingredients",
#     )


# @pytest.fixture
# def enriched_recipe_search_danish():
#     return EnrichedRecipe(
#         url="http://example.com",
#         ingredients=[
#             EnrichedIngredient(
#                 original_name="2 tomater",
#                 en_name="2 tomatoes",
#                 weight_estimate=WeightEstimate(
#                     ingredient="2 tomatoes",
#                     weight_calculation="2 tomatoes = 200g",
#                     weight_in_kg=0.2,
#                 ),
#                 co2_per_kg_search=CO2SearchResult(
#                     ingredient="2 tomatoes",
#                     result=2.0,
#                     explanation="Search result",
#                     unit="kg CO2e / kg",
#                 ),
#             ),
#             EnrichedIngredient(
#                 original_name="1 liter mælk",
#                 en_name="1 liter of milk",
#                 weight_estimate=WeightEstimate(
#                     ingredient="1 liter of milk",
#                     weight_calculation="1 liter = 1kg",
#                     weight_in_kg=1.0,
#                 ),
#                 co2_per_kg_search=CO2SearchResult(
#                     ingredient="1 liter of milk",
#                     result=1.0,
#                     explanation="Search result",
#                     unit="kg CO2e / kg",
#                 ),
#             ),
#             EnrichedIngredient(
#                 original_name="3 store æg",
#                 en_name="3 large eggs",
#                 weight_estimate=WeightEstimate(
#                     ingredient="3 large eggs",
#                     weight_calculation="3 large eggs = 150g",
#                     weight_in_kg=0.15,
#                 ),
#                 co2_per_kg_search=CO2SearchResult(
#                     ingredient="3 large eggs",
#                     result=3.0,
#                     explanation="Search result",
#                     unit="kg CO2e / kg",
#                 ),
#             ),
#         ],
#         persons=4,
#         instructions="Mix ingredients",
#     )


@pytest.mark.parametrize(
    "enriched_recipe, negligeble_threshold, expected_output",
    [
        (
            "enriched_recipe_db_english",
            # Languages.English,
            0.1,
            RecipeCO2Output(
                total_co2_kg=1.9,
                number_of_persons=4,
                co2_per_person_kg=0.5,
                avg_meal_emission_per_person_range_kg=[1.3, 2.2],
                ingredients=[
                    IngredientOutput(
                        name="1 liter of milk",
                        ingredient_id="456",
                        weight_kg=1.0,
                        co2_per_kg=1.0,
                        co2_kg=1.0,
                        calculation_notes="1.0 kg * 1.0 kg CO2e/kg (DB) = 1.0 kg CO2e",
                        weight_estimation_notes="1 liter = 1kg",
                        co2_emission_notes="Best match in CO2 database is: milk",
                    ),
                    IngredientOutput(
                        name="2 tomatoes",
                        ingredient_id="123",
                        weight_kg=0.2,
                        co2_per_kg=2.5,
                        co2_kg=0.5,
                        calculation_notes="0.2 kg * 2.5 kg CO2e/kg (DB) = 0.5 kg CO2e",
                        weight_estimation_notes="2 tomatoes = 200g",
                        co2_emission_notes="Best match in CO2 database is: tomatoes, canned",
                    ),
                    IngredientOutput(
                        name="3 large eggs",
                        ingredient_id="789",
                        weight_kg=0.15,
                        co2_per_kg=3.0,
                        co2_kg=0.45,
                        calculation_notes="0.15 kg * 3.0 kg CO2e/kg (DB) = 0.45 kg CO2e",
                        weight_estimation_notes="3 large eggs = 150g",
                        co2_emission_notes="Best match in CO2 database is: eggs",
                    ),
                ],
            ),
        ),
        (
            "enriched_recipe_search_english",
            # Languages.English,
            0.1,
            RecipeCO2Output(
                total_co2_kg=1.8,
                number_of_persons=4,
                co2_per_person_kg=0.5,
                avg_meal_emission_per_person_range_kg=[1.3, 2.2],
                ingredients=[
                    IngredientOutput(
                        name="1 liter of milk",
                        ingredient_id=None,
                        weight_kg=1.0,
                        co2_per_kg=1.0,
                        co2_kg=1.0,
                        calculation_notes="1.0 kg * 1.0 kg CO2e/kg (Search) = 1.0 kg CO2e",
                        weight_estimation_notes="1 liter = 1kg",
                        co2_emission_notes="Found by search. Notes on finding search are; 'Search result'",
                    ),
                    IngredientOutput(
                        name="3 large eggs",
                        ingredient_id=None,
                        weight_kg=0.15,
                        co2_per_kg=3.0,
                        co2_kg=0.45,
                        calculation_notes="0.15 kg * 3.0 kg CO2e/kg (Search) = 0.45 kg CO2e",
                        weight_estimation_notes="3 large eggs = 150g",
                        co2_emission_notes="Found by search. Notes on finding search are; 'Search result'",
                    ),
                    IngredientOutput(
                        name="2 tomatoes",
                        ingredient_id=None,
                        weight_kg=0.2,
                        co2_per_kg=2.0,
                        co2_kg=0.4,
                        calculation_notes="0.2 kg * 2.0 kg CO2e/kg (Search) = 0.4 kg CO2e",
                        weight_estimation_notes="2 tomatoes = 200g",
                        co2_emission_notes="Found by search. Notes on finding search are; 'Search result'",
                    ),
                ],
            ),
        ),
        # (
        #     "enriched_recipe_db_danish",
        #     Languages.Danish,
        #     0.1,
        #     (
        #         "----------------------------------------"
        #         "\nSamlet CO2-udslip: 1.9 kg CO2e"
        #         "\nEstimeret antal personer: 4"
        #         "\nEmission pr. person: 0.5 kg CO2e / pr. person"
        #         "\nGennemsnitligt aftensmad udledning pr. person: 1.3 - 2.2 kg CO2e / pr. person"
        #         "\n----------------------------------------"
        #         "\nBeregningsmetoden pr. ingrediens er: X kg * Y kg CO2e / kg = Z kg CO2e"
        #         "\n2 tomater: 0.2 kg * 2.5 kg CO2e / kg (DB) = 0.5 kg CO2e"
        #         "\n1 liter mælk: 1.0 kg * 1.0 kg CO2e / kg (DB) = 1.0 kg CO2e"
        #         "\n3 store æg: 0.15 kg * 3.0 kg CO2e / kg (DB) = 0.45 kg CO2e"
        #         "\n----------------------------------------"
        #         "\n\nForklaring:"
        #         "\n(DB) - Data fra SQL Database (https://denstoreklimadatabase.dk)"
        #         "\n(Søgning) - Data opnået fra søgning"
        #         "\n\nKommentarer:"
        #         "\nFor 2 tomater:"
        #         "\n- Vægt: 2 tomatoes = 200g"
        #         "\n- DB: Database entry"
        #         "\nFor 1 liter mælk:"
        #         "\n- Vægt: 1 liter = 1kg"
        #         "\n- DB: Database entry"
        #         "\nFor 3 store æg:"
        #         "\n- Vægt: 3 large eggs = 150g"
        #         "\n- DB: Database entry"
        #     ),
        # ),
        # (
        #     "enriched_recipe_search_danish",
        #     Languages.Danish,
        #     0.1,
        #     (
        #         "----------------------------------------"
        #         "\nSamlet CO2-udslip: 1.8 kg CO2e"
        #         "\nEstimeret antal personer: 4"
        #         "\nEmission pr. person: 0.5 kg CO2e / pr. person"
        #         "\nGennemsnitligt aftensmad udledning pr. person: 1.3 - 2.2 kg CO2e / pr. person"
        #         "\n----------------------------------------"
        #         "\nBeregningsmetoden pr. ingrediens er: X kg * Y kg CO2e / kg = Z kg CO2e"
        #         "\n2 tomater: 0.2 kg * 2.0 kg CO2e / kg (Search) = 0.4 kg CO2e"
        #         "\n1 liter mælk: 1.0 kg * 1.0 kg CO2e / kg (Search) = 1.0 kg CO2e"
        #         "\n3 store æg: 0.15 kg * 3.0 kg CO2e / kg (Search) = 0.45 kg CO2e"
        #         "\n----------------------------------------"
        #         "\n\nForklaring:"
        #         "\n(DB) - Data fra SQL Database (https://denstoreklimadatabase.dk)"
        #         "\n(Søgning) - Data opnået fra søgning"
        #         "\n\nKommentarer:"
        #         "\nFor 2 tomater:"
        #         "\n- Vægt: 2 tomatoes = 200g"
        #         "\n- Søgning: Search result"
        #         "\nFor 1 liter mælk:"
        #         "\n- Vægt: 1 liter = 1kg"
        #         "\n- Søgning: Search result"
        #         "\nFor 3 store æg:"
        #         "\n- Vægt: 3 large eggs = 150g"
        #         "\n- Søgning: Search result"
        #     ),
        # ),
    ],
    ids=[
        "test_db_english",
        "test_search_english",
        # "test_db_danish",
        # "test_search_danish",
    ],
)
def test_generate_output(
    request: pytest.FixtureRequest,
    enriched_recipe: str,
    negligeble_threshold: float,
    expected_output: str,
) -> None:
    recipe = request.getfixturevalue(enriched_recipe)
    result = generate_output_model(
        enriched_recipe=recipe,
        negligeble_threshold=negligeble_threshold,
        number_of_persons=4,
    )
    assert result == expected_output
