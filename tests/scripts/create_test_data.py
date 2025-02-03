import asyncio
import json
import os

from tests.data_paths import FINAL_ENRICHED_RECIPE_DIR
from tests.load_files import (
    get_expected_enriched_recipe,
    get_expected_rag_co2_estimates,
    get_expected_weight_estimates,
)
from tests.scripts.create_extracted_recipe import (
    process_and_store_recipe as extract_recipe_and_save,
)
from tests.scripts.create_rag_co2_estimates import save_rag_co2_estimates
from tests.scripts.create_weight_estimates import save_weight_estimates
from tests.urls import TEST_URLS

# Directory to store the results
os.makedirs(FINAL_ENRICHED_RECIPE_DIR, exist_ok=True)


async def process_and_store_enriched_recipe(file_name: str, url: str):
    # Extract the recipe and save it
    await extract_recipe_and_save(file_name, url)
    enriched_recipe = get_expected_enriched_recipe(file_name)

    # Estimate weights and save them
    await save_weight_estimates(file_name, url)
    weight_estimates = get_expected_weight_estimates(file_name)

    # Estimate CO2 emissions and save them
    await save_rag_co2_estimates(file_name, url)
    co2_estimates = get_expected_rag_co2_estimates(file_name)

    enriched_recipe.update_with_weight_estimates(weight_estimates)
    enriched_recipe.update_with_co2_per_kg_db(co2_estimates)

    # Store the final enriched recipe with translations as JSON
    final_output_filepath = os.path.join(FINAL_ENRICHED_RECIPE_DIR, file_name)
    with open(final_output_filepath, "w", encoding="utf-8") as file:
        json.dump(enriched_recipe.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored final enriched JSON output for {url} in {final_output_filepath}")


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(process_and_store_enriched_recipe(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
