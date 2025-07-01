from __future__ import annotations

from collections.abc import Iterable

from food_co2_estimator.chains.rag_co2_estimator import (
    above_weight_threshold,
    should_include_ingredient,
)
from food_co2_estimator.pydantic_models.estimator import (
    IngredientOutput,
    RecipeCO2Output,
)
from food_co2_estimator.pydantic_models.recipe_extractor import (
    EnrichedIngredient,
    EnrichedRecipe,
)

# Average Danish dinner emissions (kg CO₂e / capita)
MIN_DINNER_EMISSION_PER_CAPITA = 1.3
MAX_DINNER_EMISSION_PER_CAPITA = 2.2


def generate_output_model(
    enriched_recipe: EnrichedRecipe,
    negligeble_threshold: float,
    number_of_persons: int | None,
) -> RecipeCO2Output:
    """Create a :class:`RecipeCO2Output` for *enriched_recipe*."""
    (
        ingredients,
        total_co2,
        total_energy,
        total_fat,
        total_carb,
        total_protein,
    ) = build_ingredient_outputs(
        enriched_recipe.ingredients,
        negligeble_threshold,
    )
    co2_per_person = calculate_co2_per_person(total_co2, number_of_persons)

    return create_recipe_output(
        enriched_recipe,
        ingredients,
        total_co2,
        number_of_persons,
        co2_per_person,
        total_energy,
        total_fat,
        total_carb,
        total_protein,
    )


def build_ingredient_outputs(
    ingredients: Iterable[EnrichedIngredient],
    negligeble_threshold: float,
) -> tuple[list[IngredientOutput], float, float, float, float, float]:
    """Return ingredient outputs and total values for the recipe."""
    outputs: list[IngredientOutput] = []
    total_co2: float = 0.0
    total_energy = 0.0
    total_fat = 0.0
    total_carb = 0.0
    total_protein = 0.0

    for ingredient in ingredients:
        output, co2, energy, fat, carb, protein = evaluate_single_ingredient(
            ingredient, negligeble_threshold
        )
        outputs.append(output)
        if co2 is not None:
            total_co2 += co2
        if energy is not None:
            total_energy += energy
        if fat is not None:
            total_fat += fat
        if carb is not None:
            total_carb += carb
        if protein is not None:
            total_protein += protein

    # highest emitters first
    outputs.sort(key=lambda x: (x.co2_kg is not None, x.co2_kg), reverse=True)
    return outputs, total_co2, total_energy, total_fat, total_carb, total_protein


def evaluate_single_ingredient(
    ingredient: EnrichedIngredient,
    negligeble_threshold: float,
) -> tuple[
    IngredientOutput,
    float | None,
    float | None,
    float | None,
    float | None,
    float | None,
]:
    """Route an ingredient to the correct builder, returning (output, co2)."""
    weight = ingredient.weight_estimate

    if weight is None or weight.weight_in_kg is None:
        return create_output_no_weight(ingredient), None, None, None, None, None

    if not should_include_ingredient(ingredient, negligeble_threshold):
        return (
            create_output_negligible(ingredient, negligeble_threshold),
            None,
            None,
            None,
            None,
            None,
        )

    return create_output_calculated(ingredient)  # may still yield co2=None


def create_output_no_weight(ingredient: EnrichedIngredient) -> IngredientOutput:
    """Ingredient has no weight estimate—CO₂ cannot be calculated."""
    weight_notes = (
        ingredient.weight_estimate.weight_calculation
        if ingredient.weight_estimate
        else "Could not estimate weight"
    )
    return IngredientOutput(
        name=ingredient.name,
        ingredient_id=None,
        weight_kg=None,
        co2_kg=None,
        co2_per_kg=None,
        calculation_notes="Without weight estimate can CO₂ not be calculated",
        weight_estimation_notes=weight_notes,
        co2_emission_notes=None,
    )


def create_output_negligible(
    ingredient: EnrichedIngredient,
    negligeble_threshold: float,
) -> IngredientOutput:
    """Ingredient weight is below the negligible threshold."""
    weight = ingredient.weight_estimate  # guaranteed present
    weight_in_kg = weight.weight_in_kg if weight else None
    weight_kg = round(weight_in_kg, 3) if weight_in_kg is not None else None
    note = (
        f"Weight on {weight_kg} kg is negligible"
        if not above_weight_threshold(ingredient, negligeble_threshold)
        else "Ingredient is ignored in calculation"
    )
    return IngredientOutput(
        name=ingredient.name,
        ingredient_id=None,
        weight_kg=weight_kg,
        co2_kg=None,
        co2_per_kg=None,
        calculation_notes=note,
        weight_estimation_notes=weight.weight_calculation
        if weight
        else "Could not estimate weight",
        co2_emission_notes=note,
    )


def create_output_calculated(
    ingredient: EnrichedIngredient,
) -> tuple[
    IngredientOutput,
    float | None,
    float | None,
    float | None,
    float | None,
    float | None,
]:
    """Ingredient has weight; try to compute its CO₂ emission."""
    weight = ingredient.weight_estimate
    weight_in_kg = weight.weight_in_kg if weight else None
    co2_data = ingredient.co2_per_kg_db
    co2_per_kg = co2_data.co2_per_kg if co2_data else None

    computed_co2: float | None = None
    if co2_per_kg is not None and weight_in_kg is not None:
        computed_co2 = round(co2_per_kg * weight_in_kg, 2)
    weight_in_kg = round(weight_in_kg, 2) if weight_in_kg is not None else None
    co2_per_kg = round(co2_per_kg, 2) if co2_per_kg is not None else None

    def calc_nutrient(value_100g: float | None) -> float | None:
        if value_100g is None or weight_in_kg is None:
            return None
        return round(value_100g * 10 * weight_in_kg, 2)

    energy = calc_nutrient(co2_data.energy_kj_100g if co2_data else None)
    fat = calc_nutrient(co2_data.fat_g_100g if co2_data else None)
    carb = calc_nutrient(co2_data.carbohydrate_g_100g if co2_data else None)
    protein = calc_nutrient(co2_data.protein_g_100g if co2_data else None)
    calc_note = (
        f"{weight_in_kg} kg * {co2_per_kg} kg CO₂e/kg = {computed_co2} kg CO₂e"
        if co2_per_kg is not None
        else "Kan ikke beregne CO₂-udledning uden CO₂ pr. kg"
    )
    emission_note = (
        f"Bedste match i CO₂-databasen er: {co2_data.closest_match_name}"
        if co2_data
        else "Kan ikke finde CO₂-udledning"
    )

    output = IngredientOutput(
        name=ingredient.name,
        ingredient_id=co2_data.ingredient_id if co2_data else None,
        weight_kg=weight_in_kg,
        co2_per_kg=co2_per_kg,
        co2_kg=computed_co2,
        calculation_notes=calc_note,
        weight_estimation_notes=weight.weight_calculation
        if weight
        else "Could not estimate weight",
        co2_emission_notes=emission_note,
        energy_kj=energy,
        fat_g=fat,
        carbohydrate_g=carb,
        protein_g=protein,
    )
    return output, computed_co2, energy, fat, carb, protein


def calculate_co2_per_person(total_co2: float, persons: int | None) -> float | None:
    """Return per-capita CO₂ or *None* if `persons` is invalid."""
    if persons is None or persons <= 0:
        return None
    raw_value = total_co2 / persons
    decimals = 1 if raw_value >= 0.05 else 2
    return round(raw_value, decimals)


def create_recipe_output(
    recipe: EnrichedRecipe,
    ingredients: list[IngredientOutput],
    total_co2: float,
    persons: int | None,
    co2_per_person: float | None,
    total_energy: float,
    total_fat: float,
    total_carb: float,
    total_protein: float,
) -> RecipeCO2Output:
    """Assemble the top-level :class:`RecipeCO2Output`."""
    return RecipeCO2Output(
        title=recipe.title,
        url=recipe.url,
        total_co2_kg=round(total_co2, 1),
        number_of_persons=persons,
        co2_per_person_kg=co2_per_person,
        avg_meal_emission_per_person=,
        ingredients=ingredients,
        total_energy_kj=round(total_energy, 2) if total_energy else None,
        total_fat_g=round(total_fat, 2) if total_fat else None,
        total_carbohydrate_g=round(total_carb, 2) if total_carb else None,
        total_protein_g=round(total_protein, 2) if total_protein else None,
    )
