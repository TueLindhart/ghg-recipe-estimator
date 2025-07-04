import pytest

from food_co2_estimator.language.detector import Languages
from food_co2_estimator.pydantic_models.co2_estimator import CO2Emissions, CO2perKg
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
    ExtractedRecipe,
)
from food_co2_estimator.pydantic_models.weight_estimator import (
    WeightEstimate,
    WeightEstimates,
)


@pytest.fixture
def recipe():
    return EnrichedRecipe(
        title="Dummy Recipe",
        language=Languages.English,
        url="http://example.com",
        ingredients=[
            EnrichedIngredient(
                name="1 dåse tomater",
            ),
            EnrichedIngredient(
                name="2 agurker",
            ),
            EnrichedIngredient(
                name="1 dåse tomater",
            ),
        ],
        persons=2,
        instructions="Mix ingredients",
    )


def test_update_with_weight_estimates(recipe: EnrichedRecipe):
    weight_estimates = WeightEstimates(
        weight_estimates=[
            WeightEstimate(
                ingredient="1 dåse tomater",
                weight_calculation="1 dåse tomater = 200g",
                weight_in_kg=0.2,
            ),
        ]
    )

    recipe.update_with_weight_estimates(weight_estimates)
    for ingredient, weight in zip(recipe.ingredients, [0.2, None, 0.2]):
        if weight:
            assert (
                ingredient.weight_estimate is not None
                and ingredient.weight_estimate.weight_in_kg == weight
            )
        else:
            assert ingredient.weight_estimate is None


def test_update_with_co2_per_kg_db(recipe: EnrichedRecipe):
    co2_emissions = CO2Emissions(
        emissions=[
            CO2perKg(
                closest_match_explanation="Matches 'tomatoes, canned' best.",
                closest_match_name="tomatoes, canned",
                ingredient="1 dåse tomater",
                ingredient_id="123",
                co2_per_kg=2.5,
                unit="kg",
            )
        ]
    )

    recipe.update_with_co2_per_kg_db(co2_emissions)

    for ingredient, co2 in zip(recipe.ingredients, [2.5, None, 2.5]):
        if co2:
            assert (
                ingredient.co2_per_kg_db is not None
                and ingredient.co2_per_kg_db.co2_per_kg == co2
            )
        else:
            assert ingredient.co2_per_kg_db is None


def test_get_ingredients_lists(recipe: EnrichedRecipe):
    names = recipe.get_ingredient_names()
    assert names == ["1 dåse tomater", "2 agurker", "1 dåse tomater"]


def test_from_extracted_recipe():
    ingredients = ["1 dåse tomater", "2 agurker", "1 dåse tomater"]
    extracted = ExtractedRecipe(
        title="Dummy Recipe",
        ingredients=ingredients,
        persons=2,
        instructions="Mix ingredients",
    )

    enriched = EnrichedRecipe.from_extracted_recipe(
        url="http://example.com", extracted_recipe=extracted
    )

    assert enriched.url == "http://example.com"
    assert len(enriched.ingredients) == 3
    assert enriched.persons == 2
    assert enriched.instructions == "Mix ingredients"
    for idx, expected in enumerate(ingredients):
        assert enriched.ingredients[idx].name == expected
