from food_co2_estimator.pydantic_models.response_models import ComparisonResponse
from food_co2_estimator.utils.output_generator import (
    AVG_EMISSION_PER_CAPITA_PER_MEAL,
    AVG_EMISSION_PER_CAPITA_PER_DAY,
    BUDGET_EMISSION_PER_CAPITA_PER_MEAL,
    BUDGET_EMISSION_PER_CAPITA_PER_DAY,
)

REFERENCE_SEGMENT_KG: float = 45  # 100 %


def compare_co2(kgco2: float) -> ComparisonResponse:
    """
    Compare an amount of CO₂ to the reference segment.
    """
    if kgco2 <= 0:
        raise ValueError("kgco2 must be > 0")

    ratio = kgco2 / REFERENCE_SEGMENT_KG
    return ComparisonResponse(
        input_co2_kg=kgco2,
        reference_kg=REFERENCE_SEGMENT_KG,
        ratio=ratio,
        helperText=f"{kgco2} kg CO₂ er {ratio:.2%} af en tur fra København til Aalborg i en benzinbil",
        avg_emission_per_person_per_meal=AVG_EMISSION_PER_CAPITA_PER_MEAL,
        avg_emission_per_person_per_day=AVG_EMISSION_PER_CAPITA_PER_DAY,
        budget_emission_per_person_per_meal=BUDGET_EMISSION_PER_CAPITA_PER_MEAL,
        budget_emission_per_person_per_day=BUDGET_EMISSION_PER_CAPITA_PER_DAY,
    )
