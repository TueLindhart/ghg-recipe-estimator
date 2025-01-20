import pytest

from food_co2_estimator.chains.recipe_extractor import ExtractedRecipe, extract_recipe

KNOWN_RECIPE_REPLACEMENTS = {
    "½": "0.5",
    "⅓": "0.33",
    "⅔": "0.66",
    "¼": "0.25",
    "¾": "0.75",
}


@pytest.mark.asyncio
async def test_extract_recipe_with_persons_in_url(
    monkeypatch: pytest.MonkeyPatch, dummy_recipe: ExtractedRecipe
):
    text = "Sample recipe text"
    url = "http://example.com?antal=4"
    verbose = False

    async def mock_ainvoke(*args, **kwargs):
        return dummy_recipe

    class MockChain:
        async def ainvoke(self, *args, **kwargs):
            return await mock_ainvoke(*args, **kwargs)

    def mock_get_recipe_extractor_chain(*args, **kwargs):
        return MockChain()

    monkeypatch.setattr(
        "food_co2_estimator.chains.recipe_extractor.get_recipe_extractor_chain",
        mock_get_recipe_extractor_chain,
    )

    result = await extract_recipe(text, url, verbose)

    assert result.persons == 4
    assert result == dummy_recipe


# @pytest.mark.asyncio(loop_scope="function")
# async def test_extract_recipe_chain(
#     markdown_and_expected_extracted_recipe: tuple[str, ExtractedRecipe],
# ):
#     markdown_content, expected_extracted_recipe = markdown_and_expected_extracted_recipe
#     result = await extract_recipe(markdown_content, "www.example.com", verbose=False)

#     ingredients = [ingredient for ingredient in result.ingredients]
#     ingredients = [
#         ingredient.replace(k, v)
#         for ingredient in ingredients
#         for k, v in KNOWN_RECIPE_REPLACEMENTS.items()
#     ]
#     for ingredient, expected_ingredient in zip(
#         result.ingredients, expected_extracted_recipe.ingredients
#     ):
#         assert ingredient == expected_ingredient

#     assert result.persons == expected_extracted_recipe.persons
