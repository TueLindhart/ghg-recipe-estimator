import asyncio
import json
import os

from dotenv import load_dotenv

from food_co2_estimator.chains.rag_co2_estimator import (
    NEGLIGIBLE_THRESHOLD,
    get_co2_emissions,
)
from food_co2_estimator.pydantic_models.co2_estimator import CO2Emissions
from tests.conftest import get_expected_enriched_recipe
from tests.data_paths import CO2_EMISSIONS_DIR
from tests.load_files import get_expected_weight_estimates
from tests.urls import TEST_URLS

# Directory to store the results
os.makedirs(CO2_EMISSIONS_DIR, exist_ok=True)

# Load environment variables from the project root
load_dotenv()


async def save_rag_co2_estimates(file_name: str, url: str) -> CO2Emissions:
    enriched_recipe = get_expected_enriched_recipe(file_name)
    weight_estimates = get_expected_weight_estimates(file_name)
    enriched_recipe.update_with_weight_estimates(weight_estimates)
    rag_co2_estimates = await get_co2_emissions(
        verbose=False, recipe=enriched_recipe, negligeble_threshold=NEGLIGIBLE_THRESHOLD
    )

    enriched_recipe.update_with_co2_per_kg_db(rag_co2_estimates)
    assert not all(
        item.co2_per_kg_db is None for item in enriched_recipe.ingredients
    ), f"Missing CO2 estimates for {url}"

    # Store the result as JSON
    output_filepath = os.path.join(CO2_EMISSIONS_DIR, file_name + ".json")
    with open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(rag_co2_estimates.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored JSON output for {url} in {output_filepath}")

    return rag_co2_estimates


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(save_rag_co2_estimates(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
