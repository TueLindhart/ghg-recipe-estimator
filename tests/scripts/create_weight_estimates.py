import asyncio
import json
import os

from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from tests.conftest import get_extracted_recipe
from tests.urls import TEST_URLS

# Directory to store the results
output_dir = "tests/data/extracted_weight_estimates_json"
os.makedirs(output_dir, exist_ok=True)

# Directory containing the website text files
input_dir = "tests/data/recipe_json"


async def save_weight_estimates(file_name: str, url: str):
    extracted_recipe = get_extracted_recipe(file_name)
    enriched_recipe = EnrichedRecipe.from_extracted_recipe(
        extracted_recipe=extracted_recipe,
        url=url,
    )
    weight_estimate = await get_weight_estimates(verbose=False, recipe=enriched_recipe)

    # Store the result as JSON
    output_filepath = os.path.join(output_dir, file_name + ".json")
    with open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(weight_estimate.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored JSON output for {url} in {output_filepath}")


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(save_weight_estimates(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
