from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe

# Constants for average Danish dinner emission per person
MIN_DINNER_EMISSION_PER_CAPITA = 1.3
MAX_DINNER_EMISSION_PER_CAPITA = 2.2

from typing import List, Optional

from pydantic import BaseModel


class IngredientOutput(BaseModel):
    name: str
    weight_kg: Optional[float] = None
    co2_kg: Optional[float] = None
    comment: Optional[str] = None


class RecipeCO2Output(BaseModel):
    total_co2_kg: float
    number_of_persons: Optional[int] = None
    co2_per_person_kg: Optional[float] = None
    avg_meal_emission_per_person_range_kg: List[float]
    ingredients: List[IngredientOutput]


# Constants for average Danish dinner emission per person
MIN_DINNER_EMISSION_PER_CAPITA = 1.3
MAX_DINNER_EMISSION_PER_CAPITA = 2.2


def generate_output_model(
    enriched_recipe: EnrichedRecipe,
    negligible_threshold: float,
    number_of_persons: int | None,
) -> RecipeCO2Output:
    total_co2 = 0.0
    ingredients_list = []

    # Process each ingredient in the enriched recipe.
    for ingredient in enriched_recipe.ingredients:
        weight_estimate = ingredient.weight_estimate
        co2_data = ingredient.co2_per_kg_db
        search_result = ingredient.co2_per_kg_search

        # If no weight estimate is available, add an ingredient with an error comment.
        if weight_estimate is None or weight_estimate.weight_in_kg is None:
            ingredients_list.append(
                IngredientOutput(
                    name=ingredient.original_name,
                    weight_kg=None,
                    co2_kg=None,
                    comment="unable to estimate weight",
                )
            )
            continue

        # If the weight is negligible, mark it as such and set CO2 to 0.
        if weight_estimate.weight_in_kg <= negligible_threshold:
            wt = round(weight_estimate.weight_in_kg, 3)
            ingredients_list.append(
                IngredientOutput(
                    name=ingredient.original_name,
                    weight_kg=wt,
                    co2_kg=0,
                    comment=f"weight on {wt} kg is negligible",
                )
            )
            continue

        computed_co2 = None
        comment = ""
        # Prefer CO2 data from the DB.
        if co2_data and co2_data.co2_per_kg:
            computed_co2 = round(co2_data.co2_per_kg * weight_estimate.weight_in_kg, 2)
            comment = (
                f"{round(weight_estimate.weight_in_kg, 2)} kg * "
                f"{round(co2_data.co2_per_kg, 2)} kg CO2e/kg (DB) = {computed_co2} kg CO2e"
            )
        # Fallback to using search result data.
        elif search_result and search_result.result:
            computed_co2 = round(search_result.result * weight_estimate.weight_in_kg, 2)
            comment = (
                f"{round(weight_estimate.weight_in_kg, 2)} kg * "
                f"{round(search_result.result, 2)} kg CO2e/kg (Search) = {computed_co2} kg CO2e"
            )
        else:
            comment = "CO2e per kg not found"

        if computed_co2 is not None:
            total_co2 += computed_co2

        ingredients_list.append(
            IngredientOutput(
                name=ingredient.original_name,
                weight_kg=round(weight_estimate.weight_in_kg, 3),
                co2_kg=computed_co2,
                comment=comment,
            )
        )

    # Calculate per-person CO2 if number_of_persons is provided and valid.
    if number_of_persons is not None and number_of_persons > 0:
        co2_per_person = round(total_co2 / number_of_persons, 1)
    else:
        co2_per_person = None

    # Create the top-level output model.
    output_model = RecipeCO2Output(
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
