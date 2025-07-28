import asyncio
import json
import os

from dotenv import load_dotenv

from food_co2_estimator.chains.weight_estimator import get_weight_estimates
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimates
from tests.conftest import get_expected_enriched_recipe
from tests.data_paths import WEIGHT_EST_DIR
from tests.urls import TEST_URLS

# Directory to store the results
os.makedirs(WEIGHT_EST_DIR, exist_ok=True)

# Load environment variables from the project root
load_dotenv()


async def save_weight_estimates(file_name: str, url: str) -> WeightEstimates:
    enriched_recipe = get_expected_enriched_recipe(file_name)
    weight_estimate = await get_weight_estimates(verbose=False, recipe=enriched_recipe)

    # Store the result as JSON
    output_filepath = os.path.join(WEIGHT_EST_DIR, file_name + ".json")
    with open(output_filepath, "w", encoding="utf-8") as file:
        json.dump(weight_estimate.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored JSON output for {url} in {output_filepath}")
    return weight_estimate


async def main():
    tasks = []
    for file_name, url in TEST_URLS.items():
        tasks.append(save_weight_estimates(file_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
