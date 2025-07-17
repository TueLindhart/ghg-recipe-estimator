from enum import Enum

from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    url: str
    use_cache: bool = Field(
        default_factory=lambda: True, description="Use cached results if available"
    )
    store_in_cache: bool = Field(
        default_factory=lambda: True,
        description="Store results in cache for future use",
    )


class StartEstimateResponse(BaseModel):
    uid: str
    status: str


class JobStatus(str, Enum):
    ERROR = "Error"
    COMPLETED = "Completed"
    PROCESSING = "Processing"
    EXTRACTING_TEXT = "Text"
    EXTRACTING_RECIPE = "Recipe"
    TRANSLATING = "Translating"
    ESTIMATING_WEIGHTS = "Weights"
    ESTIMATING_CO2 = "RAGCO2"
    ESTIMATING_SEARCH_CO2 = "SearchCO2"
    PREPARING_OUTPUT = "Preparing"


class JobResult(BaseModel):
    status: JobStatus
    result: str | None = None


class AvgEmissionPerPerson(BaseModel):
    meal: float = Field(
        description="Average meal emission per person in kg",
    )
    day: float = Field(
        description="Average daily emission per person in kg",
    )


class BudgetEmissionPerPerson(BaseModel):
    meal: float = Field(
        description="Budget for one meal's emission per person in kg",
    )
    day: float = Field(
        description="Daily emission budget per person in kg",
    )


class Comparison(BaseModel):
    """Pydantic model returned by the FastAPI endpoint."""

    label: str = Field(
        ...,
        description="Label for the comparison, e.g., 'Diesel Car', 'Flight CPH to Aalborg', 'Washing Machine'",
    )
    input_co2_kg: float = Field(..., gt=0, description="Compared CO₂ (kg)")
    reference_co2_kg: float = Field(
        ...,
        description="Reference CO₂ value for comparison (kg)",
    )
    comparison: float = Field(
        ...,
        description="Comparison value in relation to the reference segment",
    )
    help_text: str = Field(
        ...,
        description="Text to help the user understand the comparison (in Danish)",
    )

    @classmethod
    def create(
        cls,
        input_co2_kg: float,
    ):
        """Create a comparison instance. Should be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the create method")


class ComparisonResponse(BaseModel):
    """Pydantic model returned by the FastAPI endpoint."""

    comparisons: list[Comparison] = Field(
        ...,
        description="List of comparisons for different CO₂ values",
    )
    avg_emission_per_person: AvgEmissionPerPerson = Field(
        ...,
        description="Average emissions per person for a meal and a day",
    )
    budget_emission_per_person: BudgetEmissionPerPerson = Field(
        ...,
        description="Budget emissions per person for a meal and a day",
    )
