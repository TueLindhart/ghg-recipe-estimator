import re

from langchain_core.runnables import RunnableSerializable

from food_co2_estimator.logging_wrapper import log_with_url
from food_co2_estimator.prompt_templates.recipe_extractor import RECIPE_EXTRACTOR_PROMPT
from food_co2_estimator.pydantic_models.recipe_extractor import ExtractedRecipe
from food_co2_estimator.utils.openai_model import get_model

NUMBER_PERSONS_REGEX = r".*\?antal=(\d+)"


def get_recipe_extractor_chain(verbose: bool = False) -> RunnableSerializable:
    llm = get_model(pydantic_model=ExtractedRecipe, verbose=verbose)

    chain = RECIPE_EXTRACTOR_PROMPT | llm
    return chain


def extract_person_from_url(url) -> int | None:
    match = re.match(NUMBER_PERSONS_REGEX, url)
    if match:
        return int(match.group(1))


@log_with_url
async def extract_recipe(text: str, url: str, verbose: bool) -> ExtractedRecipe:
    recipe_extractor_chain = get_recipe_extractor_chain(verbose=verbose)
    recipe: ExtractedRecipe = await recipe_extractor_chain.ainvoke({"input": text})

    # If number is provided in url, then use that instead of llm estimate
    persons = extract_person_from_url(url)
    recipe.persons = persons if isinstance(persons, int) else recipe.persons

    return recipe
