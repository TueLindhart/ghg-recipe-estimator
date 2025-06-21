from food_co2_estimator.chains.rag_co2_estimator import (
    above_weight_threshold,
    should_include_ingredient,
)
from food_co2_estimator.pydantic_models.estimator import (
    IngredientOutput,
    RecipeCO2Output,
)
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe

# Constants for average Danish dinner emission per person
MIN_DINNER_EMISSION_PER_CAPITA = 1.3
MAX_DINNER_EMISSION_PER_CAPITA = 2.2


def generate_output_model(
    enriched_recipe: EnrichedRecipe,
    negligeble_threshold: float,
    number_of_persons: int | None,
) -> RecipeCO2Output:
    total_co2 = 0.0
    ingredients_list = []

    # Process each ingredient in the enriched recipe.
    for ingredient in enriched_recipe.ingredients:
        weight_estimate = ingredient.weight_estimate
        co2_data = ingredient.co2_per_kg_db

        # If no weight estimate is available, add an ingredient with an error comment.
        if weight_estimate is None or weight_estimate.weight_in_kg is None:
            weight_estimation_notes = (
                weight_estimate.weight_calculation
                if weight_estimate
                else "Could not estimate weight"
            )
            ingredients_list.append(
                IngredientOutput(
                    name=ingredient.name,
                    ingredient_id=None,
                    weight_kg=None,
                    co2_kg=None,
                    co2_per_kg=None,
                    calculation_notes="Without weight estimate can CO2 not be calculated",
                    weight_estimation_notes=weight_estimation_notes,
                    co2_emission_notes=None,
                )
            )
            continue

        # If the weight is negligible, mark it as such and set CO2 to 0.
        if not should_include_ingredient(ingredient, negligeble_threshold):
            weight_estimation_notes = weight_estimate.weight_calculation
            wt = round(weight_estimate.weight_in_kg, 3)
            calculation_notes = (
                f"Weight on {wt} kg is negligible"
                if not above_weight_threshold(ingredient, negligeble_threshold)
                else "Ingredient is ignored in calculation"
            )
            ingredients_list.append(
                IngredientOutput(
                    name=ingredient.name,
                    ingredient_id=None,
                    weight_kg=wt,
                    co2_kg=None,
                    co2_per_kg=None,
                    co2_emission_notes=calculation_notes,
                    calculation_notes=calculation_notes,
                    weight_estimation_notes=weight_estimation_notes,
                )
            )
            continue

        co2_per_kg = co2_data.co2_per_kg if co2_data is not None else None

        computed_co2 = (
            round(co2_per_kg * weight_estimate.weight_in_kg, 2) if co2_per_kg else None
        )
        calculation_note = (
            f"{round(weight_estimate.weight_in_kg, 2)} kg * "
            f"{round(co2_per_kg, 2)} kg CO2e/kg = {computed_co2} kg CO2e"
            if co2_per_kg
            else "Cannot calculate CO2 emission without CO2 per kg"
        )

        co2_emission_notes = (
            f"Best match in CO2 database is: {co2_data.closest_match_name}"
            if co2_data is not None
            else "Unable to find CO2 emission"
        )
        ingredient_id = (
            ingredient.co2_per_kg_db.ingredient_id if ingredient.co2_per_kg_db else None
        )

        if computed_co2 is not None:
            total_co2 += computed_co2

        ingredients_list.append(
            IngredientOutput(
                name=ingredient.name,
                ingredient_id=ingredient_id,
                weight_kg=round(weight_estimate.weight_in_kg, 3),
                co2_per_kg=co2_per_kg,
                co2_kg=computed_co2,
                calculation_notes=calculation_note,
                weight_estimation_notes=weight_estimate.weight_calculation,
                co2_emission_notes=co2_emission_notes,
            )
        )

    # Sort ingredients by CO2 emission in descending order.
    ingredients_list.sort(key=lambda x: (x.co2_kg is not None, x.co2_kg), reverse=True)

    # Calculate per-person CO2 if number_of_persons is provided and valid.
    if number_of_persons is not None and number_of_persons > 0:
        co2_per_person_raw = total_co2 / number_of_persons
        n_decimal_places = 1 if co2_per_person_raw >= 0.05 else 2
        co2_per_person = round(total_co2 / number_of_persons, n_decimal_places)
    else:
        co2_per_person = None

    # Create the top-level output model.
    output_model = RecipeCO2Output(
        title=enriched_recipe.title,
        url=enriched_recipe.url,
        total_co2_kg=round(total_co2, 1),
        number_of_persons=number_of_persons,
        co2_per_person_kg=co2_per_person,
        avg_meal_emission_per_person_range_kg=[
            MIN_DINNER_EMISSION_PER_CAPITA,
            MAX_DINNER_EMISSION_PER_CAPITA,
        ],
        ingredients=ingredients_list,
    )

    return output_model
