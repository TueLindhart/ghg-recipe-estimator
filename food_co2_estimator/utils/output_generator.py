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

# https://concito.dk/files/media/document/Danmarks%20globale%20forbrugsudledninger.pdf
# Average Danish dinner emissions (kg CO₂e / capita)
# 13 [ton / year]  * 20 % / 365 [days] = 0.00712 ton CO₂e / day
# 0.00721 ton CO₂e / day * 1000 = 7.12 kg CO₂e / day
AVG_EMISSION_PER_CAPITA_PER_DAY = 7.1
# Average Danish dinner emissions (kg CO₂e / meal)
# 7.12 kg CO₂e / day / 4 meals per day = 1.78 kg CO₂e / meal
AVG_EMISSION_PER_CAPITA_PER_MEAL = 1.8

# https://concito.dk/en/concito-bloggen/her-faar-du-mest-ernaering-klimaaftrykket-0?utm_source=chatgpt.com
BUDGET_EMISSION_PER_CAPITA_PER_DAY = 2.0
BUDGET_EMISSION_PER_CAPITA_PER_MEAL = 0.5


def generate_output_model(
    enriched_recipe: EnrichedRecipe,
    negligeble_threshold: float,
    number_of_persons: int | None,
) -> RecipeCO2Output:
    """Create a :class:`RecipeCO2Output` for *enriched_recipe*."""
    (
        ingredients,
        total_co2,
        energy_per_person,
        fat_per_person,
        carb_per_person,
        protein_per_person,
    ) = build_ingredient_outputs(
        enriched_recipe.ingredients,
        negligeble_threshold,
        number_of_persons,
    )
    co2_per_person = calculate_co2_per_person(total_co2, number_of_persons)

    return create_recipe_output(
        enriched_recipe,
        ingredients,
        total_co2,
        number_of_persons,
        co2_per_person,
        energy_per_person,
        fat_per_person,
        carb_per_person,
        protein_per_person,
    )


def build_ingredient_outputs(
    ingredients: Iterable[EnrichedIngredient],
    negligeble_threshold: float,
    number_of_persons: int | None = None,
) -> tuple[
    list[IngredientOutput],
    float,
    float | None,
    float | None,
    float | None,
    float | None,
]:
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

    # Calculate per-person values if number_of_persons is available
    energy_per_person = (
        total_energy / number_of_persons
        if number_of_persons and total_energy > 0
        else None
    )
    fat_per_person = (
        total_fat / number_of_persons if number_of_persons and total_fat > 0 else None
    )
    carb_per_person = (
        total_carb / number_of_persons if number_of_persons and total_carb > 0 else None
    )
    protein_per_person = (
        total_protein / number_of_persons
        if number_of_persons and total_protein > 0
        else None
    )

    # highest emitters first
    outputs.sort(key=lambda x: (x.co2_kg is not None, x.co2_kg), reverse=True)
    return (
        outputs,
        total_co2,
        energy_per_person,
        fat_per_person,
        carb_per_person,
        protein_per_person,
    )


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
    energy_per_person: float | None,
    fat_per_person: float | None,
    carb_per_person: float | None,
    protein_per_person: float | None,
) -> RecipeCO2Output:
    """Assemble the top-level :class:`RecipeCO2Output`."""
    return RecipeCO2Output(
        title=recipe.title,
        url=recipe.url,
        total_co2_kg=round(total_co2, 1),
        number_of_persons=persons,
        co2_per_person_kg=co2_per_person,
        avg_emission_per_person_per_meal=AVG_EMISSION_PER_CAPITA_PER_MEAL,
        avg_emission_per_person_per_day=AVG_EMISSION_PER_CAPITA_PER_DAY,
        budget_emission_per_person_per_meal=BUDGET_EMISSION_PER_CAPITA_PER_MEAL,
        budget_emission_per_person_per_day=BUDGET_EMISSION_PER_CAPITA_PER_DAY,
        ingredients=ingredients,
        energy_per_person_kj=round(energy_per_person, 0) if energy_per_person else None,
        fat_per_person_g=round(fat_per_person, 0) if fat_per_person else None,
        carbohydrate_per_person_g=round(carb_per_person, 0)
        if carb_per_person
        else None,
        protein_per_person_g=round(protein_per_person, 0)
        if protein_per_person
        else None,
    )
