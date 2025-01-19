import pytest

from food_co2_estimator.language.detector import Languages
from food_co2_estimator.pydantic_models.co2_estimator import CO2perKg
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)
from food_co2_estimator.pydantic_models.search_co2_estimator import CO2SearchResult
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimate
from food_co2_estimator.utils.output_generator import generate_output


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
                    ingredient="2 tomatoes",
                    co2_per_kg=2.5,
                    explanation="Database entry",
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
                    ingredient="1 liter of milk",
                    co2_per_kg=1.0,
                    explanation="Database entry",
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
                    ingredient="3 large eggs",
                    co2_per_kg=3.0,
                    explanation="Database entry",
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


@pytest.fixture
def enriched_recipe_db_danish():
    return EnrichedRecipe(
        url="http://example.com",
        ingredients=[
            EnrichedIngredient(
                original_name="2 tomater",
                en_name="2 tomatoes",
                weight_estimate=WeightEstimate(
                    ingredient="2 tomatoes",
                    weight_calculation="2 tomatoes = 200g",
                    weight_in_kg=0.2,
                ),
                co2_per_kg_db=CO2perKg(
                    ingredient="2 tomatoes",
                    co2_per_kg=2.5,
                    explanation="Database entry",
                    unit="kg CO2e / kg",
                ),
            ),
            EnrichedIngredient(
                original_name="1 liter mælk",
                en_name="1 liter of milk",
                weight_estimate=WeightEstimate(
                    ingredient="1 liter of milk",
                    weight_calculation="1 liter = 1kg",
                    weight_in_kg=1.0,
                ),
                co2_per_kg_db=CO2perKg(
                    ingredient="1 liter of milk",
                    co2_per_kg=1.0,
                    explanation="Database entry",
                    unit="kg CO2e / kg",
                ),
            ),
            EnrichedIngredient(
                original_name="3 store æg",
                en_name="3 large eggs",
                weight_estimate=WeightEstimate(
                    ingredient="3 large eggs",
                    weight_calculation="3 large eggs = 150g",
                    weight_in_kg=0.15,
                ),
                co2_per_kg_db=CO2perKg(
                    ingredient="3 large eggs",
                    co2_per_kg=3.0,
                    explanation="Database entry",
                    unit="kg CO2e / kg",
                ),
            ),
        ],
        persons=4,
        instructions="Mix ingredients",
    )


@pytest.fixture
def enriched_recipe_search_danish():
    return EnrichedRecipe(
        url="http://example.com",
        ingredients=[
            EnrichedIngredient(
                original_name="2 tomater",
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
                original_name="1 liter mælk",
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
                original_name="3 store æg",
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


@pytest.mark.parametrize(
    "enriched_recipe, language, negligeble_threshold, expected_output",
    [
        (
            "enriched_recipe_db_english",
            Languages.English,
            0.1,
            (
                "----------------------------------------"
                "\nTotal CO2 emission: 1.9 kg CO2e"
                "\nEstimated number of persons: 4"
                "\nEmission pr. person: 0.5 kg CO2e / pr. person"
                "\nAvg. Danish dinner emission pr person: 1.3 - 2.2 kg CO2e / pr. person"
                "\n----------------------------------------"
                "\nThe calculation method per ingredient is: X kg * Y kg CO2e / kg = Z kg CO2e"
                "\n2 tomatoes: 0.2 kg * 2.5 kg CO2e / kg (DB) = 0.5 kg CO2e"
                "\n1 liter of milk: 1.0 kg * 1.0 kg CO2e / kg (DB) = 1.0 kg CO2e"
                "\n3 large eggs: 0.15 kg * 3.0 kg CO2e / kg (DB) = 0.45 kg CO2e"
                "\n----------------------------------------"
                "\n\nLegends:"
                "\n(DB) - Data from SQL Database (https://denstoreklimadatabase.dk)"
                "\n(Search) - Data obtained from search"
                "\n\nComments:"
                "\nFor 2 tomatoes:"
                "\n- Weight: 2 tomatoes = 200g"
                "\n- DB: Database entry"
                "\nFor 1 liter of milk:"
                "\n- Weight: 1 liter = 1kg"
                "\n- DB: Database entry"
                "\nFor 3 large eggs:"
                "\n- Weight: 3 large eggs = 150g"
                "\n- DB: Database entry"
            ),
        ),
        (
            "enriched_recipe_search_english",
            Languages.English,
            0.1,
            (
                "----------------------------------------"
                "\nTotal CO2 emission: 1.8 kg CO2e"
                "\nEstimated number of persons: 4"
                "\nEmission pr. person: 0.5 kg CO2e / pr. person"
                "\nAvg. Danish dinner emission pr person: 1.3 - 2.2 kg CO2e / pr. person"
                "\n----------------------------------------"
                "\nThe calculation method per ingredient is: X kg * Y kg CO2e / kg = Z kg CO2e"
                "\n2 tomatoes: 0.2 kg * 2.0 kg CO2e / kg (Search) = 0.4 kg CO2e"
                "\n1 liter of milk: 1.0 kg * 1.0 kg CO2e / kg (Search) = 1.0 kg CO2e"
                "\n3 large eggs: 0.15 kg * 3.0 kg CO2e / kg (Search) = 0.45 kg CO2e"
                "\n----------------------------------------"
                "\n\nLegends:"
                "\n(DB) - Data from SQL Database (https://denstoreklimadatabase.dk)"
                "\n(Search) - Data obtained from search"
                "\n\nComments:"
                "\nFor 2 tomatoes:"
                "\n- Weight: 2 tomatoes = 200g"
                "\n- Search: Search result"
                "\nFor 1 liter of milk:"
                "\n- Weight: 1 liter = 1kg"
                "\n- Search: Search result"
                "\nFor 3 large eggs:"
                "\n- Weight: 3 large eggs = 150g"
                "\n- Search: Search result"
            ),
        ),
        (
            "enriched_recipe_db_danish",
            Languages.Danish,
            0.1,
            (
                "----------------------------------------"
                "\nSamlet CO2-udslip: 1.9 kg CO2e"
                "\nEstimeret antal personer: 4"
                "\nEmission pr. person: 0.5 kg CO2e / pr. person"
                "\nGennemsnitligt aftensmad udledning pr. person: 1.3 - 2.2 kg CO2e / pr. person"
                "\n----------------------------------------"
                "\nBeregningsmetoden pr. ingrediens er: X kg * Y kg CO2e / kg = Z kg CO2e"
                "\n2 tomater: 0.2 kg * 2.5 kg CO2e / kg (DB) = 0.5 kg CO2e"
                "\n1 liter mælk: 1.0 kg * 1.0 kg CO2e / kg (DB) = 1.0 kg CO2e"
                "\n3 store æg: 0.15 kg * 3.0 kg CO2e / kg (DB) = 0.45 kg CO2e"
                "\n----------------------------------------"
                "\n\nForklaring:"
                "\n(DB) - Data fra SQL Database (https://denstoreklimadatabase.dk)"
                "\n(Søgning) - Data opnået fra søgning"
                "\n\nKommentarer:"
                "\nFor 2 tomater:"
                "\n- Vægt: 2 tomatoes = 200g"
                "\n- DB: Database entry"
                "\nFor 1 liter mælk:"
                "\n- Vægt: 1 liter = 1kg"
                "\n- DB: Database entry"
                "\nFor 3 store æg:"
                "\n- Vægt: 3 large eggs = 150g"
                "\n- DB: Database entry"
            ),
        ),
        (
            "enriched_recipe_search_danish",
            Languages.Danish,
            0.1,
            (
                "----------------------------------------"
                "\nSamlet CO2-udslip: 1.8 kg CO2e"
                "\nEstimeret antal personer: 4"
                "\nEmission pr. person: 0.5 kg CO2e / pr. person"
                "\nGennemsnitligt aftensmad udledning pr. person: 1.3 - 2.2 kg CO2e / pr. person"
                "\n----------------------------------------"
                "\nBeregningsmetoden pr. ingrediens er: X kg * Y kg CO2e / kg = Z kg CO2e"
                "\n2 tomater: 0.2 kg * 2.0 kg CO2e / kg (Search) = 0.4 kg CO2e"
                "\n1 liter mælk: 1.0 kg * 1.0 kg CO2e / kg (Search) = 1.0 kg CO2e"
                "\n3 store æg: 0.15 kg * 3.0 kg CO2e / kg (Search) = 0.45 kg CO2e"
                "\n----------------------------------------"
                "\n\nForklaring:"
                "\n(DB) - Data fra SQL Database (https://denstoreklimadatabase.dk)"
                "\n(Søgning) - Data opnået fra søgning"
                "\n\nKommentarer:"
                "\nFor 2 tomater:"
                "\n- Vægt: 2 tomatoes = 200g"
                "\n- Søgning: Search result"
                "\nFor 1 liter mælk:"
                "\n- Vægt: 1 liter = 1kg"
                "\n- Søgning: Search result"
                "\nFor 3 store æg:"
                "\n- Vægt: 3 large eggs = 150g"
                "\n- Søgning: Search result"
            ),
        ),
    ],
)
def test_generate_output(
    request: pytest.FixtureRequest,
    enriched_recipe: str,
    language: Languages,
    negligeble_threshold: float,
    expected_output: str,
) -> None:
    recipe = request.getfixturevalue(enriched_recipe)
    result = generate_output(
        enriched_recipe=recipe,
        negligeble_threshold=negligeble_threshold,
        number_of_persons=4,
        language=language,
    )
    assert result == expected_output
