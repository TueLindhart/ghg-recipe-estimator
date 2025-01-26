import json
import os

from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedRecipe,
    ExtractedRecipe,
)
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimates
from tests.data_paths import (
    ENRICHED_RECIPE_DIR,
    EXTRACTED_RECIPE_DIR,
    TEXT_INPUT_DIR,
    WEIGHT_EST_DIR,
)


def create_path(folder: str, file_name: str, file_type: str) -> str:
    return os.path.join(folder, file_name + f".{file_type}")


def load_json_file(folder: str, file_name: str) -> dict:
    expected_output_filepath = create_path(
        folder=folder, file_name=file_name, file_type="json"
    )
    with open(expected_output_filepath, "r", encoding="utf-8") as file:
        expected_output = json.load(file)
    return expected_output


def load_text_file(folder: str, file_name: str) -> str:
    input_filepath = create_path(folder=folder, file_name=file_name, file_type="md")
    with open(input_filepath, "r", encoding="utf-8") as file:
        markdown_text = file.read()
    return markdown_text


def get_recipe_markdown_text(file_name: str) -> str:
    return load_text_file(folder=TEXT_INPUT_DIR, file_name=file_name)


def get_expected_extracted_recipe(file_name: str) -> ExtractedRecipe:
    extracted_recipe_json = load_json_file(
        folder=EXTRACTED_RECIPE_DIR, file_name=file_name
    )
    return ExtractedRecipe(**extracted_recipe_json)


def get_expected_enriched_recipe(file_name: str) -> EnrichedRecipe:
    enriched_recipe_json = load_json_file(
        folder=ENRICHED_RECIPE_DIR, file_name=file_name
    )
    return EnrichedRecipe(**enriched_recipe_json)


def get_expected_weight_estimates(file_name: str) -> WeightEstimates:
    weight_estimates_json = load_json_file(folder=WEIGHT_EST_DIR, file_name=file_name)
    return WeightEstimates(**weight_estimates_json)
