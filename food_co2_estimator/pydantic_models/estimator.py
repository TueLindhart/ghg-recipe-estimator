import logging
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


class RunParams(pydantic.BaseModel):
    url: str
    uid: str = pydantic.Field(default_factory=get_uuid)
    negligeble_threshold: float = NEGLIGIBLE_THRESHOLD
    use_cache: bool = pydantic.Field(default_factory=env_use_cache)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, RunParams):
            return False
        if self.url != value.url:
            return False
        if self.negligeble_threshold != value.negligeble_threshold:
            return False
        return True


class LogParams(pydantic.BaseModel):
    logging_level: int = logging.INFO
    verbose: bool = False


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
