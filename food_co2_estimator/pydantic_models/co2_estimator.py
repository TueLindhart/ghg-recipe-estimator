from typing import List, Optional

from pydantic import BaseModel, Field


class CO2perKg(BaseModel):
    closest_match_explanation: str = Field(
        description="A concise reference to the instructions or specific cases used to determine why the selected "
        "emission option is the closest match. The explanation should indicate which rules or examples "
        "in the provided matching instructions were applied."
    )
    ingredientId: str = Field(
        description="The id of the ingredient picked used to reference the db",
    )
    closest_match_name: str = Field(
        description="Name of the closest match in emission database. Example: 'Tomatoes, canned."
        "Write 'No match' if there is no suitable match."
    )
    ingredient: str = Field(
        description="Name of ingredient exactly transcribed from ingredients input with no modifications. '2 cans of tomatoes.'"
    )
    unit: str = Field(description="The unit which is 'kg CO2e per kg'")
    co2_per_kg: Optional[float] = Field(
        description="'kg CO2 per kg' directly 'copy-pasted' from closest match. Set to 'none' if there is no good match.",
        default=None,
    )


class CO2Emissions(BaseModel):
    emissions: List[CO2perKg]
