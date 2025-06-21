from typing import List

from pydantic import BaseModel, Field

from food_co2_estimator.pydantic_models.co2_estimator import CO2Emissions, CO2perKg
from food_co2_estimator.pydantic_models.weight_estimator import (
    WeightEstimate,
    WeightEstimates,
)


class ExtractedRecipe(BaseModel):
    """Class containing recipe information"""

    title: str | None = Field(
        description="This field should contain the title of the recipe."
    )
    ingredients: List[str] = Field(
        description="This field should contain a list of ingredients in the recipe"
    )
    persons: int | None = Field(
        description="This field should contain number of persons recipe if for."
    )
    instructions: str | None = Field(
        description="This field should contain instructions for recipe."
    )


class EnrichedIngredient(BaseModel):
    """Class containing enriched ingredient information"""

    name: str
    weight_estimate: WeightEstimate | None = None
    co2_per_kg_db: CO2perKg | None = None

    @classmethod
    def from_list(cls, ingredients: list[str]) -> List["EnrichedIngredient"]:
        return [cls(name=ingredient) for ingredient in ingredients]

    def is_name_match(self, name: str) -> bool:
        return self.name.strip() == name.strip()

    def set_weight_estimate(self, weight_estimate: WeightEstimate):
        if self.name.strip() == weight_estimate.ingredient.strip():
            self.weight_estimate = weight_estimate

    def set_co2_per_kg_db(self, co2_per_kg: CO2perKg):
        if self.name.strip() == co2_per_kg.ingredient.strip():
            self.co2_per_kg_db = co2_per_kg


class EnrichedRecipe(ExtractedRecipe):
    url: str
    ingredients: list[EnrichedIngredient]

    def get_ingredient_names(self) -> list[str]:
        return [ingredient.name for ingredient in self.ingredients]

    @classmethod
    def from_extracted_recipe(
        cls,
        url,
        extracted_recipe: ExtractedRecipe,
    ) -> "EnrichedRecipe":
        return cls(
            title=extracted_recipe.title,
            url=url,
            ingredients=EnrichedIngredient.from_list(extracted_recipe.ingredients),
            persons=extracted_recipe.persons,
            instructions=extracted_recipe.instructions,
        )

    def get_match_objects(
        self, obj: WeightEstimate | CO2perKg
    ) -> list[EnrichedIngredient]:
        matched_ingredients = []
        for ingredient in self.ingredients:
            if (
                ingredient.name is not None
                and ingredient.name.strip() == obj.ingredient.strip()
            ):
                matched_ingredients.append(ingredient)
        return matched_ingredients

    def update_with_weight_estimates(self, weight_estimates: WeightEstimates):
        for weight_estimate in weight_estimates.weight_estimates:
            ingredients = self.get_match_objects(weight_estimate)
            for ingredient in ingredients:
                ingredient.set_weight_estimate(weight_estimate)

    def update_with_co2_per_kg_db(self, co2_emissions: CO2Emissions):
        for co2_per_kg in co2_emissions.emissions:
            ingredients = self.get_match_objects(co2_per_kg)
            for ingredient in ingredients:
                ingredient.set_co2_per_kg_db(co2_per_kg)
