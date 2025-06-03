import json
import os

from food_co2_estimator.chains.rag_co2_estimator import NEGLIGIBLE_THRESHOLD
from food_co2_estimator.utils.output_generator import generate_output_model
from tests.data_paths import FINAL_ENRICHED_RECIPE_DIR, OUTPUT_RECIPE_DIR
from tests.load_files import (
    get_expected_enriched_recipe,
    get_expected_rag_co2_estimates,
    get_expected_weight_estimates,
)
from tests.urls import TEST_URLS

# Directory to store the results
os.makedirs(FINAL_ENRICHED_RECIPE_DIR, exist_ok=True)
os.makedirs(OUTPUT_RECIPE_DIR, exist_ok=True)


def process_and_store_enriched_recipe(file_name: str, url: str):
    # Extract the recipe and save it
    enriched_recipe = get_expected_enriched_recipe(file_name)

    # Estimate weights and save them
    weight_estimates = get_expected_weight_estimates(file_name)

    # Estimate CO2 emissions and save them
    co2_estimates = get_expected_rag_co2_estimates(file_name)

    enriched_recipe.update_with_weight_estimates(weight_estimates)
    enriched_recipe.update_with_co2_per_kg_db(co2_estimates)

    # Store the final enriched recipe with translations as JSON
    final_enriched_recipe_dir = os.path.join(
        FINAL_ENRICHED_RECIPE_DIR, file_name + ".json"
    )
    with open(final_enriched_recipe_dir, "w", encoding="utf-8") as file:
        json.dump(enriched_recipe.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored final enriched JSON output for {url} in {final_enriched_recipe_dir}")

    output_model = generate_output_model(
        enriched_recipe=enriched_recipe,
        negligible_threshold=NEGLIGIBLE_THRESHOLD,
        number_of_persons=enriched_recipe.persons,
    )
    # Store the final enriched recipe with translations as JSON
    final_output_filepath = os.path.join(OUTPUT_RECIPE_DIR, file_name + ".json")
    with open(final_output_filepath, "w", encoding="utf-8") as file:
        json.dump(output_model.model_dump(), file, ensure_ascii=False, indent=4)
    print(f"Stored final enriched JSON output for {url} in {final_output_filepath}")


def main():
    for file_name, url in TEST_URLS.items():
        process_and_store_enriched_recipe(file_name, url)


if __name__ == "__main__":
    main()
