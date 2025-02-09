from typing import List

from pydantic import BaseModel, Field


class IngredientOutput(BaseModel):
    name: str = Field(description="Name of ingredient.")
    ingredient_id: str | None = Field(description="ingredient Id from vector DB")
    weight_kg: float | None = Field(
        description="Weight",
    )
    co2_per_kg: float | None = Field(
        description="kg CO2e / kg",
    )
    co2_kg: float | None = Field(description="CO2 Emission in kg")
    calculation_notes: str | None = Field(description="Comment")
    weight_estimation_notes: str | None = Field(
        description="Comment on weight estimation"
    )
    co2_emission_notes: str | None = Field(description="Comment on CO2 emission")


class RecipeCO2Output(BaseModel):
    total_co2_kg: float
    number_of_persons: int | None = None
    co2_per_person_kg: float | None = None
    avg_meal_emission_per_person_range_kg: List[float]
    ingredients: List[IngredientOutput]
