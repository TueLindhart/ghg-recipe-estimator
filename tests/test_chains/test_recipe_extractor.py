from difflib import SequenceMatcher

import pytest

from food_co2_estimator.chains.recipe_extractor import ExtractedRecipe, extract_recipe

MIN_STRING_SIMILARITY_SCORE = 0.1


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


def string_similarity(text1: str, text2: str) -> float:
    return SequenceMatcher(None, text1, text2).ratio()


@pytest.mark.asyncio
async def test_extract_recipe_chain(
    markdown_and_expected_extracted_recipe_fixture: tuple[str, ExtractedRecipe],
):
    markdown_content, expected_extracted_recipe = (
        markdown_and_expected_extracted_recipe_fixture
    )
    result = await extract_recipe(markdown_content, "www.example.com", verbose=False)

    for ingredient, expected_ingredient in zip(
        result.ingredients, expected_extracted_recipe.ingredients
    ):
        sim_score = string_similarity(ingredient, expected_ingredient)
        if "salt" in ingredient or "peber" in ingredient:
            continue

        assert (
            sim_score > MIN_STRING_SIMILARITY_SCORE
        ), f" '{ingredient}' and '{expected_ingredient}': Similarity score {sim_score} is not greater than {MIN_STRING_SIMILARITY_SCORE}"

    assert (
        result.persons == expected_extracted_recipe.persons
    ), f"Expected {expected_extracted_recipe.persons} persons, but got {result.persons}"
