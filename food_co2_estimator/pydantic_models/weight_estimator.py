from typing import List, Optional

from pydantic import BaseModel, Field


class WeightEstimate(BaseModel):
    ingredient: str = Field(
        description="Exact name of the ingredient without any changes. Must be of type str.",
    )
    weight_calculation: str = Field(
        description="Description of how weights are estimated. Must be of type str.",
    )
    weight_in_kg: Optional[float] = Field(
        description="Weight provided in kg. Must be float. Defaults to None",
        default=None,
    )


class WeightEstimates(BaseModel):
    weight_estimates: List[WeightEstimate] = Field(
        description="List of 'WeightEstimate' per ingredient. Must be of type list[WeightEstimate].",
    )
