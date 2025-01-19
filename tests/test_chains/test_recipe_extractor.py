import pytest

from food_co2_estimator.chains.recipe_extractor import ExtractedRecipe, extract_recipe


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


# @pytest.mark.asyncio
# async def test_extract_recipe_without_persons_in_url(
#     markdown_content: str, expected_extracted_recipe: ExtractedRecipe
# ):
#     result = await extract_recipe(markdown_content, "www.example.com", verbose=False)
#     assert result.model_dump_json() == expected_extracted_recipe.model_dump_json()
