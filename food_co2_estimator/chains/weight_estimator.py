from typing import Any

from langchain.schema.runnable import RunnableSerializable

from food_co2_estimator.language.detector import Languages
from food_co2_estimator.logger_utils import log_with_url
from food_co2_estimator.prompt_templates.weight_estimator import get_weight_est_prompt
from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe
from food_co2_estimator.pydantic_models.weight_estimator import WeightEstimates
from food_co2_estimator.utils.llm_model import LLMFactory


def get_weight_estimator_chain(
    verbose: bool = False,
    language: Languages = Languages.English,
) -> RunnableSerializable[Any, Any]:
    llm = LLMFactory(output_model=WeightEstimates, verbose=verbose).get_model()
    prompt = get_weight_est_prompt(language)
    chain = prompt | llm
    return chain


@log_with_url
async def get_weight_estimates(
    *,
    verbose: bool,
    recipe: EnrichedRecipe,
) -> WeightEstimates:
    weight_estimator_chain = get_weight_estimator_chain(
        verbose=verbose, language=recipe.language
    )

    servings = recipe.persons if recipe.persons is not None else "Estimate"
    weight_output: WeightEstimates = await weight_estimator_chain.ainvoke(
        {"input": recipe.get_ingredient_names(), "servings": servings},
    )  # type: ignore

    return weight_output
