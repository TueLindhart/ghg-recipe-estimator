import asyncio
import json
import os

from food_co2_estimator.chains.recipe_extractor import extract_recipe
from food_co2_estimator.chains.translator import get_translation_chain
from food_co2_estimator.language.detector import detect_language
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from tests.urls import TEST_URLS

# Directory to store the results
extracted_output_dir = "tests/data/recipe_json"
os.makedirs(extracted_output_dir, exist_ok=True)

# Directory to store the enriched recipes with translations
enriched_output_dir = "tests/data/enriched_recipe_json"
os.makedirs(enriched_output_dir, exist_ok=True)

# Directory containing the website text files
input_dir = "tests/data/website_text"


async def process_and_store_recipe(file_name: str, url: str):
    # Read the content from the markdown file
    input_filepath = os.path.join(input_dir, file_name + ".md")
    with open(input_filepath, "r", encoding="utf-8") as file:
        text = file.read()

    # Extract the recipe
    recipe = await extract_recipe(text, url, verbose=False)

    # Store the extracted recipe as JSON
    extracted_output_filepath = os.path.join(extracted_output_dir, file_name + ".json")
    with open(extracted_output_filepath, "w", encoding="utf-8") as file:
        json.dump(recipe.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored JSON output for {url} in {extracted_output_filepath}")

    # Detect language in ingredients
    enriched_recipe = EnrichedRecipe.from_extracted_recipe(url, recipe)
    language = detect_language(enriched_recipe)

    # Translate the recipe if needed
    translator = get_translation_chain()
    enriched_recipe = await translator.ainvoke(
        {"recipe": enriched_recipe, "language": language}
    )

    # Store the enriched recipe with translations as JSON
    enriched_output_filepath = os.path.join(enriched_output_dir, file_name + ".json")
    with open(enriched_output_filepath, "w", encoding="utf-8") as file:
        json.dump(enriched_recipe.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored enriched JSON output for {url} in {enriched_output_filepath}")


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(process_and_store_recipe(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
