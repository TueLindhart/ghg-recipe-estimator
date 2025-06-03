# co2_comparison.py
"""
Isolated logic for comparing an arbitrary CO₂ amount to a fixed reference

Nothing in here is FastAPI-specific; it can be unit-tested in pure Python.
"""

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
REFERENCE_SEGMENT_KG: float = 45  # 100 %
# ---------------------------------------------------------------------------


class ComparisonResponse(BaseModel):
    """Pydantic model returned by the FastAPI endpoint."""

    input_co2_kg: float = Field(..., gt=0, description="Compared CO₂ (kg)")
    reference_kg: float = Field(..., description="Reference segment (kg)")
    ratio: float = Field(..., description="input_co2_kg / reference_kg")
    helperText: str = Field(
        ...,
        description="Human-readable explanation of the comparison result",
    )


def compare_co2(kgco2: float) -> ComparisonResponse:
    """
    Compare an amount of CO₂ to the reference segment.

    Parameters
    ----------
    kgco2 : float
        Positive CO₂ amount in kilograms.

    Returns
    -------
    ComparisonResponse
        Structured result with the ratio.
    """
    if kgco2 <= 0:
        raise ValueError("kgco2 must be > 0")

    ratio = kgco2 / REFERENCE_SEGMENT_KG
    return ComparisonResponse(
        input_co2_kg=kgco2,
        reference_kg=REFERENCE_SEGMENT_KG,
        ratio=ratio,
        helperText=f"{kgco2} kg CO₂ er {ratio:.2%} af en tur fra København til Aalborg i en benzinbil",
    )
