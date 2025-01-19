import asyncio
import json
import os

from food_co2_estimator.chains.recipe_extractor import extract_recipe
from tests.urls import TEST_URLS

# Directory to store the results
output_dir = "tests/data/recipe_json"
os.makedirs(output_dir, exist_ok=True)

# Directory containing the website text files
input_dir = "tests/data/website_text"


async def process_url(file_name, url):
    # Read the content from the markdown file
    input_filepath = os.path.join(input_dir, file_name + ".md")
    with open(input_filepath, "r", encoding="utf-8") as file:
        text = file.read()

    # Extract the recipe
    recipe = await extract_recipe(text, url, verbose=False)

    # Store the result as JSON
    output_filepath = os.path.join(output_dir, file_name + ".json")
    with open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(recipe.dict(), file, ensure_ascii=False, indent=4)
    print(f"Stored JSON output for {url} in {output_filepath}")


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(process_url(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
