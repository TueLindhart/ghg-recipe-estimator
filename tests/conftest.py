import json
import os

import pytest

from food_co2_estimator.pydantic_models.recipe_extractor import ExtractedRecipe
from tests.urls import TEST_URLS

TEXT_INPUT_DIR = "tests/data/website_text"
EXTRACTED_RECIPE_DIR = "tests/data/recipe_json"


@pytest.fixture
def dummy_recipe():
    return ExtractedRecipe(
        persons=2,
        ingredients=["ingredient1", "ingredient2"],
        instructions="instructions",
    )


@pytest.fixture(params=TEST_URLS.keys())
def markdown_and_expected_extracted_recipe(request: pytest.FixtureRequest):
    file_name = request.param
    input_filepath = os.path.join(TEXT_INPUT_DIR, file_name + ".md")
    with open(input_filepath, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    expected_output_filepath = os.path.join(EXTRACTED_RECIPE_DIR, file_name + ".json")
    with open(expected_output_filepath, "r", encoding="utf-8") as file:
        expected_output = json.load(file)
    return markdown_text, ExtractedRecipe(**expected_output)
