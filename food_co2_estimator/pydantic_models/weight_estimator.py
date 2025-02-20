from typing import List, Optional

from pydantic import BaseModel, Field


class WeightEstimate(BaseModel):
    ingredient: str = Field(
        description="Exact name of the ingredient without any changes."
    )
    weight_calculation: str = Field(
        description="Description of how weights are estimated"
    )
    weight_in_kg: Optional[float] = Field(
        description="Weight provided in kg", default=None
    )


class WeightEstimates(BaseModel):
    weight_estimates: List[WeightEstimate] = Field(
        description="List of 'WeightEstimate' per ingredient."
    )
