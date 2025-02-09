from unittest.mock import Mock

import pytest

from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.output import RecipeCO2Output
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedRecipe,
    ExtractedRecipe,
)

MAX_TOTAL_RATIO_DIFFERENCE = 0.1


@pytest.mark.asyncio
async def test_async_estimator(
    monkeypatch: pytest.MonkeyPatch,
    markdown_and_expected_enriched_recipe: tuple[
        str, ExtractedRecipe, EnrichedRecipe, RecipeCO2Output
    ],
):
    (
        markdown_text,
        expected_extracted_recipe,
        expected_enriched_recipe,
        expected_output,
    ) = markdown_and_expected_enriched_recipe

    # Mock get_markdown_from_url
    mock_get_markdown_from_url = Mock(return_value=markdown_text)
    monkeypatch.setattr(
        "food_co2_estimator.main.get_markdown_from_url",
        mock_get_markdown_from_url,
    )

    # Mock extract_recipe
    async def mock_extract_recipe(text: str, url: str, verbose: bool):
        return expected_extracted_recipe

    monkeypatch.setattr("food_co2_estimator.main.extract_recipe", mock_extract_recipe)

    # Mock get_translation_chain
    mock_translation_chain = Mock()

    async def mock_ainvoke(inputs):
        return expected_enriched_recipe

    mock_translation_chain.ainvoke = mock_ainvoke
    monkeypatch.setattr(
        "food_co2_estimator.main.get_translation_chain",
        Mock(return_value=mock_translation_chain),
    )

    # Call the function
    output = await async_estimator(
        url="http://example.com",
        verbose=False,
    )

    assert not isinstance(output, str), output

    # Assert no need to use search
    for ingredient in output.ingredients:
        if ingredient.co2_emission_notes is not None:
            assert (
                "Found by search." not in ingredient.co2_emission_notes
            ), "Ingredient found by search"

    n_persons = output.number_of_persons
    assert n_persons is not None
    total_emission_per_person = output.total_co2_kg / n_persons
    expected_total_emission_per_person = expected_output.total_co2_kg / n_persons
    ratio_difference = (
        abs(total_emission_per_person - expected_total_emission_per_person)
        / expected_total_emission_per_person
    )
    assert ratio_difference <= MAX_TOTAL_RATIO_DIFFERENCE, (
        f"Total emission per person difference in % is above max: {round(ratio_difference * 100, 2)}% > {MAX_TOTAL_RATIO_DIFFERENCE * 100}%"
        f"Total emission is result={output.total_co2_kg} kg, expected = {output.total_co2_kg} kg"
    )
