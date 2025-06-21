import asyncio
import json
import os

from food_co2_estimator.chains.recipe_extractor import extract_recipe
from food_co2_estimator.language.detector import detect_language
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from tests.data_paths import ENRICHED_RECIPE_DIR, EXTRACTED_RECIPE_DIR, TEXT_INPUT_DIR
from tests.urls import TEST_URLS

# Directory to store the results
os.makedirs(EXTRACTED_RECIPE_DIR, exist_ok=True)
os.makedirs(ENRICHED_RECIPE_DIR, exist_ok=True)


def load_file(file_name: str, file_type: str) -> str:
    """Load the content of a file based on its type."""
    file_path = os.path.join(TEXT_INPUT_DIR, f"{file_name}.{file_type}")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


async def process_and_store_recipe(file_name: str, url: str) -> EnrichedRecipe:
    # Read the content from the markdown file
    text = load_file(file_name, "md")

    # Extract the recipe
    recipe = await extract_recipe(text, url, verbose=False)

    # Store the extracted recipe as JSON
    extracted_output_filepath = os.path.join(EXTRACTED_RECIPE_DIR, file_name + ".json")
    with open(extracted_output_filepath, "w", encoding="utf-8") as file:
        json.dump(recipe.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored JSON output for {url} in {extracted_output_filepath}")

    # Detect language in ingredients
    enriched_recipe = EnrichedRecipe.from_extracted_recipe(url, recipe)
    language = detect_language(enriched_recipe)

    # Copy ingredient names as detected language (no translation)
    enriched_recipe.update_with_translations(
        enriched_recipe.get_ingredient_names(),
        enriched_recipe.instructions,
    )
    # Store the enriched recipe with translations as JSON
    enriched_output_filepath = os.path.join(ENRICHED_RECIPE_DIR, file_name + ".json")
    with open(enriched_output_filepath, "w", encoding="utf-8") as file:
        json.dump(enriched_recipe.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored enriched JSON output for {url} in {enriched_output_filepath}")
    return enriched_recipe


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(process_and_store_recipe(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
