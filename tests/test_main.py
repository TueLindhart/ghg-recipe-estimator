from unittest.mock import Mock

import pytest

from food_co2_estimator.main import async_estimator
from tests.load_files import (
    get_expected_enriched_recipe,
    get_expected_extracted_recipe,
    get_expected_rag_co2_estimates,
    get_expected_weight_estimates,
)


@pytest.fixture
def enriched_recipe_fixture():
    file_name = "valdemarsro_vegetar_enchiladas"
    return get_expected_enriched_recipe(file_name)


@pytest.fixture
def extracted_recipe_fixture():
    file_name = "valdemarsro_vegetar_enchiladas"
    return get_expected_extracted_recipe(file_name)


@pytest.fixture
def weight_estimates_fixture():
    file_name = "valdemarsro_vegetar_enchiladas"
    return get_expected_weight_estimates(file_name)


@pytest.fixture
def rag_co2_estimates_fixture():
    file_name = "valdemarsro_vegetar_enchiladas"
    return get_expected_rag_co2_estimates(file_name)


@pytest.mark.asyncio
async def test_async_estimator_static(
    monkeypatch,
    enriched_recipe_fixture,
    extracted_recipe_fixture,
    weight_estimates_fixture,
    rag_co2_estimates_fixture,
):
    # Mock get_markdown_from_url
    mock_get_markdown_from_url = Mock(return_value="Sample recipe text")
    monkeypatch.setattr(
        "food_co2_estimator.url.url2markdown.get_markdown_from_url",
        mock_get_markdown_from_url,
    )

    # Mock extract_recipe
    async def mock_extract_recipe(text, url, verbose):
        return extracted_recipe_fixture

    monkeypatch.setattr(
        "food_co2_estimator.chains.recipe_extractor.extract_recipe", mock_extract_recipe
    )

    # Mock detect_language
    mock_detect_language = Mock(return_value="da")
    monkeypatch.setattr(
        "food_co2_estimator.language.detector.detect_language", mock_detect_language
    )

    # Mock get_translation_chain
    mock_translation_chain = Mock()

    async def mock_ainvoke(inputs):
        return enriched_recipe_fixture

    mock_translation_chain.ainvoke = mock_ainvoke
    monkeypatch.setattr(
        "food_co2_estimator.chains.translator.get_translation_chain",
        Mock(return_value=mock_translation_chain),
    )

    # Mock get_weight_estimates
    async def mock_get_weight_estimates(verbose, recipe):
        return weight_estimates_fixture

    monkeypatch.setattr(
        "food_co2_estimator.chains.weight_estimator.get_weight_estimates",
        mock_get_weight_estimates,
    )

    # Mock get_co2_emissions
    async def mock_get_co2_emissions(verbose, recipe, negligeble_threshold):
        return rag_co2_estimates_fixture

    monkeypatch.setattr(
        "food_co2_estimator.chains.rag_co2_estimator.get_co2_emissions",
        mock_get_co2_emissions,
    )

    # Mock get_co2_search_emissions
    async def mock_get_co2_search_emissions(verbose, recipe, negligeble_threshold):
        return rag_co2_estimates_fixture

    monkeypatch.setattr(
        "food_co2_estimator.chains.search_co2_estimator.get_co2_search_emissions",
        mock_get_co2_search_emissions,
    )

    # Call the function
    result = await async_estimator(url=url, verbose=False)

    # Assert the results
    assert "Total CO2 emission" in result
    assert "Estimated number of persons" in result
    assert "Emission pr. person" in result
    assert "Avg. Danish dinner emission pr person" in result
    assert "The calculation method per ingredient is" in result
    assert "2 tomatoes" in result
    assert "1 liter of milk" in result
    assert "3 large eggs" in result
