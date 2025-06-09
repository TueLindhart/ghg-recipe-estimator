from deep_translator.exceptions import TranslationNotFound

from food_co2_estimator.language.translator import (
    MyTranslator,
    _translate_if_not_english,
)
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)


def _create_enriched_recipe():
    return EnrichedRecipe(
        title="Kartoffelsalat",
        url="http://example.com",
        ingredients=EnrichedIngredient.from_list(["kartofler", "gulerod"]),
        instructions="Bland kartofler og gulerod",
        persons=2,
    )


def test_translate_fallback_on_failure(mocker):
    mocker.patch.object(
        MyTranslator, "translate", side_effect=TranslationNotFound("mocked failure")
    )
    recipe = _create_enriched_recipe()
    result = _translate_if_not_english(recipe, "da")
    assert isinstance(result, EnrichedRecipe)
