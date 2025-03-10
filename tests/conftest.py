from copy import deepcopy

import pytest

from food_co2_estimator.pydantic_models.estimator import RecipeCO2Output
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedRecipe,
    ExtractedRecipe,
)
from tests.load_files import (
    get_expected_enriched_recipe,
    get_expected_estimation_output,
    get_expected_extracted_recipe,
    get_expected_rag_co2_estimates,
    get_expected_weight_estimates,
    get_recipe_markdown_text,
)
from tests.urls import TEST_URLS


@pytest.fixture(autouse=True)
def override_use_cache(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "food_co2_estimator.pydantic_models.estimator.env_use_cache", lambda: False
    )


@pytest.fixture
def dummy_recipe():
    return ExtractedRecipe(
        persons=2,
        ingredients=["ingredient1", "ingredient2"],
        instructions="instructions",
    )


@pytest.fixture(params=TEST_URLS.keys())
def markdown_and_expected_extracted_recipe_fixture(request: pytest.FixtureRequest):
    file_name = request.param
    markdown_text = get_recipe_markdown_text(file_name)

    expected_output = get_expected_extracted_recipe(file_name)
    return markdown_text, expected_output


@pytest.fixture(params=TEST_URLS.keys())
def enriched_recipe_fixture(request: pytest.FixtureRequest):
    file_name = request.param
    return file_name, get_expected_enriched_recipe(file_name)


@pytest.fixture
def enriched_recipe_with_weight_est_fixture(
    enriched_recipe_fixture: tuple[str, EnrichedRecipe],
) -> tuple[str, EnrichedRecipe]:
    file_name, enriched_recipe = enriched_recipe_fixture
    enriched_recipe = deepcopy(enriched_recipe)
    weight_estimates = get_expected_weight_estimates(file_name)
    enriched_recipe.update_with_weight_estimates(weight_estimates)
    return file_name, enriched_recipe


@pytest.fixture
def enriched_recipe_with_co2_est_fixture(
    enriched_recipe_with_weight_est_fixture: tuple[str, EnrichedRecipe],
) -> tuple[str, EnrichedRecipe]:
    file_name, enriched_recipe = enriched_recipe_with_weight_est_fixture
    enriched_recipe = deepcopy(enriched_recipe)
    co2_estimates = get_expected_rag_co2_estimates(file_name)
    enriched_recipe.update_with_co2_per_kg_db(co2_estimates)
    return file_name, enriched_recipe


@pytest.fixture(params=TEST_URLS.keys())
def markdown_and_expected_enriched_recipe(
    request: pytest.FixtureRequest,
) -> tuple[str, ExtractedRecipe, EnrichedRecipe, RecipeCO2Output]:
    file_name = request.param
    markdown_text = get_recipe_markdown_text(file_name)
    expected_extracted_recipe = get_expected_extracted_recipe(file_name)
    enriched_recipe = get_expected_enriched_recipe(file_name)
    output = get_expected_estimation_output(file_name)
    return (markdown_text, expected_extracted_recipe, enriched_recipe, output)
