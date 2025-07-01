import os
import uuid
from typing import List

import pydantic
from pydantic import BaseModel, Field

from food_co2_estimator.chains.rag_co2_estimator import NEGLIGIBLE_THRESHOLD


def get_uuid() -> str:
    return uuid.uuid4().hex


def env_use_cache():
    return os.environ.get("USE_CACHE") == "true"


def env_store_in_cache():
    return os.environ.get("STORE_IN_CACHE") == "true"


class RunParams(pydantic.BaseModel):
    url: str
    uid: str = pydantic.Field(default_factory=get_uuid)
    negligeble_threshold: float = NEGLIGIBLE_THRESHOLD
    use_cache: bool = pydantic.Field(default_factory=env_use_cache)
    store_in_cache: bool = pydantic.Field(default_factory=env_store_in_cache)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, RunParams):
            return False
        if self.url != value.url:
            return False
        if self.negligeble_threshold != value.negligeble_threshold:
            return False
        return True


class IngredientOutput(BaseModel):
    name: str = Field(description="Name of ingredient.")
    ingredient_id: str | None = Field(description="ingredient Id from vector DB")
    weight_kg: float | None = Field(
        description="Weight of ingredient in kg",
    )
    co2_per_kg: float | None = Field(
        description="Emission in kg CO2e / kg",
    )
    co2_kg: float | None = Field(description="CO2 Emission in kg")
    calculation_notes: str | None = Field(description="Comment")
    weight_estimation_notes: str | None = Field(
        description="Comment on weight estimation"
    )
    co2_emission_notes: str | None = Field(description="Comment on CO2 emission")
    energy_kj: float | None = Field(
        description="Energy contribution in kJ for this ingredient",
        default=None,
    )
    fat_g: float | None = Field(
        description="Fat contribution in grams for this ingredient",
        default=None,
    )
    carbohydrate_g: float | None = Field(
        description="Carbohydrate contribution in grams for this ingredient",
        default=None,
    )
    protein_g: float | None = Field(
        description="Protein contribution in grams for this ingredient",
        default=None,
    )


class RecipeCO2Output(BaseModel):
    """Class containing recipe CO2 output information"""

    title: str | None = Field(
        description="Title of the recipe",
        default=None,
    )
    url: str = Field(
        description="URL of the recipe",
    )
    total_co2_kg: float | None = Field(
        description="Total CO2 emission for the recipe in kg", default=None
    )
    number_of_persons: int | None = Field(
        description="Number of persons the recipe is intended for",
        default=None,
    )
    co2_per_person_kg: float | None = Field(
        description="CO2 emission per person in kg",
        default=None,
    )
    avg_meal_emission_per_person: float = Field(
        description="Average meal emission per person in kg",
    )
    ingredients: List[IngredientOutput]
    total_energy_kj: float | None = Field(
        description="Total energy for the recipe in kJ",
        default=None,
    )
    total_fat_g: float | None = Field(
        description="Total fat for the recipe in grams",
        default=None,
    )
    total_carbohydrate_g: float | None = Field(
        description="Total carbohydrates for the recipe in grams",
        default=None,
    )
    total_protein_g: float | None = Field(
        description="Total protein for the recipe in grams",
        default=None,
    )
