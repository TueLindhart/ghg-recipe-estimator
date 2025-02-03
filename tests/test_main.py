from unittest.mock import Mock

import pytest

from food_co2_estimator.main import async_estimator
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedRecipe,
    ExtractedRecipe,
)

MAX_TOTAL_RATIO_DIFFERENCE = 0.1


@pytest.mark.asyncio
async def test_async_estimator(
    monkeypatch: pytest.MonkeyPatch,
    markdown_and_expected_enriched_recipe: tuple[
        str, ExtractedRecipe, EnrichedRecipe, EnrichedRecipe
    ],
):
    (
        markdown_text,
        expected_extracted_recipe,
        expected_enriched_recipe,
        expected_final_enriched_recipe,
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
    result = await async_estimator(
        url="http://example.com",
        verbose=False,
        return_output_string=False,
    )

    assert not isinstance(result, str), result

    # Assert no need to use search
    for ingredient in result.ingredients:
        assert (
            ingredient.co2_per_kg_search is None
        ), "Estimator had to use google search"

    emission_per_ingredient = calculate_emission_per_ingredient(result)
    expected_emission_per_ingredient = calculate_emission_per_ingredient(
        expected_final_enriched_recipe
    )

    total_emission = calculate_total_emission(emission_per_ingredient)
    total_expected_emission = calculate_total_emission(expected_emission_per_ingredient)

    n_persons = expected_final_enriched_recipe.persons
    assert n_persons is not None
    total_emission_per_person = total_emission / n_persons
    expected_total_emission_per_person = total_expected_emission / n_persons
    ratio_difference = (
        abs(total_emission_per_person - expected_total_emission_per_person)
        / expected_total_emission_per_person
    )
    assert (
        ratio_difference <= MAX_TOTAL_RATIO_DIFFERENCE
    ), f"Total emission per person difference in % is above max: {round(ratio_difference * 100, 2)} > {MAX_TOTAL_RATIO_DIFFERENCE}"


def calculate_emission_per_ingredient(
    recipe: EnrichedRecipe,
) -> list[tuple[str, float]]:
    emission_per_ingredient: list[tuple[str, float]] = []
    for ingredient in recipe.ingredients:
        if (
            ingredient.weight_estimate is not None
            and ingredient.weight_estimate.weight_in_kg is not None
            and ingredient.co2_per_kg_db is not None
            and ingredient.co2_per_kg_db.co2_per_kg is not None
        ):
            weight = ingredient.weight_estimate.weight_in_kg
            co2_per_kg = ingredient.co2_per_kg_db.co2_per_kg
            emission = weight * co2_per_kg
            emission_per_ingredient.append((ingredient.original_name, emission))
    return emission_per_ingredient


def calculate_total_emission(emission_per_ingredient: list[tuple[str, float]]) -> float:
    return sum(emission for _, emission in emission_per_ingredient)
