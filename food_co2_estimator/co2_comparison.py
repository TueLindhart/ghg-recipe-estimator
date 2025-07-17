from food_co2_estimator.pydantic_models.response_models import (
    AvgEmissionPerPerson,
    BudgetEmissionPerPerson,
    Comparison,
    ComparisonResponse,
)

DIESEL_CAR_EMISSION: float = 0.127  # 0.127 kg CO₂e /

EMISSION_CPH_TO_AAL: float = 29  # kg CO₂e / passenger

DK_EMISSION_PER_KWH = 96 / 1000  # kg CO₂e / kWh
WASHING_MACHINE_KWH_PER_WASH = 0.79  # kWh / wash
WASHING_MACHINE_EMISSION_PER_WASH = (
    DK_EMISSION_PER_KWH * WASHING_MACHINE_KWH_PER_WASH
)  # kg CO₂e / wash

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


class DieselCarComparison(Comparison):
    """Comparison for diesel car emissions."""

    @classmethod
    def create(cls, input_co2_kg: float) -> "DieselCarComparison":
        comparison_value = input_co2_kg / DIESEL_CAR_EMISSION
        help_text = "kilometer i en dieselbil"
        return cls(
            label="Dieselbil",
            input_co2_kg=input_co2_kg,
            reference_co2_kg=DIESEL_CAR_EMISSION,
            comparison=int(round(comparison_value, 0)),
            help_text=help_text,
        )


class EmissionCPHToAALComparison(Comparison):
    """Comparison for emissions from Copenhagen to Aalborg flight.

    Compares how many times eating the meal would be equivalent to the CO₂ emissions
    of a flight from Copenhagen to Aalborg.
    """

    @classmethod
    def create(cls, input_co2_kg: float) -> "EmissionCPHToAALComparison":
        comparison_value = EMISSION_CPH_TO_AAL / input_co2_kg
        help_text = "måltider = én flyvetur København - Aalborg"
        return cls(
            label="Flyrejse",
            input_co2_kg=input_co2_kg,
            reference_co2_kg=EMISSION_CPH_TO_AAL,
            comparison=int(round(comparison_value, 0)),
            help_text=help_text,
        )


class WashingMachineComparison(Comparison):
    """Comparison for washing machine emissions."""

    @classmethod
    def create(cls, input_co2_kg: float) -> "WashingMachineComparison":
        comparison_value = input_co2_kg / WASHING_MACHINE_EMISSION_PER_WASH
        help_text = "gange maskinvask"
        return cls(
            label="Vaskemaskine",
            input_co2_kg=input_co2_kg,
            reference_co2_kg=WASHING_MACHINE_EMISSION_PER_WASH,
            comparison=int(round(comparison_value, 0)),
            help_text=help_text,
        )


def compare_co2(kgco2: float) -> ComparisonResponse:
    """
    Compare an amount of CO₂ to the reference segment.
    """
    if kgco2 <= 0:
        raise ValueError("kgco2 must be > 0")

    return ComparisonResponse(
        comparisons=[
            DieselCarComparison.create(kgco2),
            EmissionCPHToAALComparison.create(kgco2),
            WashingMachineComparison.create(kgco2),
        ],
        avg_emission_per_person=AvgEmissionPerPerson(
            meal=AVG_EMISSION_PER_CAPITA_PER_MEAL,
            day=AVG_EMISSION_PER_CAPITA_PER_DAY,
        ),
        budget_emission_per_person=BudgetEmissionPerPerson(
            meal=BUDGET_EMISSION_PER_CAPITA_PER_MEAL,
            day=BUDGET_EMISSION_PER_CAPITA_PER_DAY,
        ),
    )
