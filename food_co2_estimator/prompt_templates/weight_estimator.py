from langchain.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from food_co2_estimator.pydantic_models.weight_estimator import (
    WeightEstimate,
    WeightEstimates,
)
from food_co2_estimator.language.detector import Languages

# The general weight lookup table
EN_WEIGHT_RECALCULATIONS = """
1 can = 400 g = 0.4 kg
1 bouillon cube = 4 g = 0.004 kg
1 onion = 170 g = 0.170 kg
1 bell pepper = 150 g = 0.150 kg
1 can tomato paste = 140 g = 0.140 kg
1 tablespoon/tbsp. = 15 g  = 0.015 kg
1 teaspoon/tsp. = 5 g = 0.005 kg
1 potato = 170 - 300 g = 0.170 - 0.300 kg
1 carrot = 100 g = 0.100 kg
1 lemon = 85 g = 0.085 kg
1 tortilla = 30 g = 0.030 kg
1 squash = 400 g = 0.400 kg
1 clove garlic = 0.004 kg
1 dl / deciliter = 0.1 kg
rice for 1 person / serving = 125 g = 0.125 kg
Handful of herbs (basil, oregano etc.) = 0.025 kg

Examples of a bunch/bnch of an ingredient - use them as a guideline:
1 bunch/bnch parsley = 50 g = 0.050 kg
1 bunch/bnch asparagus = 500 g = 0.500 kg
1 bunch of carrots = 750 g = 0.750 kg
1 bunch/bnch tomatoes = 500 g = 0.500 kg
The weights of bunches are estimated as the highest possible weight.
"""

EN_INPUT_EXAMPLE = """
1 can chopped tomatoes
200 g pasta
500 ml water
250 grams minced meat
0.5 cauliflower
1 tsp. sugar
1 organic lemon
3 teaspoons salt
2 tbsp. spices
pepper
2 large potatoes
1 bunch asparagus
1 duck, ca. 2 kg
served with rice
"""

# Danish equivalent of the input example used to demonstrate the expected format
# when ingredients are provided in Danish.
DA_INPUT_EXAMPLE = """
1 dåse hakkede tomater
200 g pasta
500 ml vand
250 g hakket kød
0.5 blomkål
1 tsk sukker
1 økologisk citron
3 tsk salt
2 spsk krydderier
peber
2 store kartofler
1 bundt asparges
1 and, ca. 2 kg
serveres med ris
"""

# Constructing the example using Pydantic models
ANSWER_EXAMPLE_OBJ = WeightEstimates(
    weight_estimates=[
        WeightEstimate(
            ingredient="1 can chopped tomatoes",
            weight_calculation="1 can = 400 g, 1 * 400 g = 400 g = 0.4 kg",
            weight_in_kg=0.4,
        ),
        WeightEstimate(
            ingredient="200 g pasta",
            weight_calculation="200 g = 200 g = 0.2 kg",
            weight_in_kg=0.2,
        ),
        WeightEstimate(
            ingredient="500 ml water",
            weight_calculation="500 ml = 500 g, 1 * 500 g = 500 g = 0.5 kg",
            weight_in_kg=0.5,
        ),
        WeightEstimate(
            ingredient="250 grams minced meat",
            weight_calculation="250 g = 250 g = 0.25 kg",
            weight_in_kg=0.25,
        ),
        WeightEstimate(
            ingredient="0.5 cauliflower",
            weight_calculation="1 cauliflower = 500 g, 0.5 * 500 g = 250 g = 0.25 kg",
            weight_in_kg=0.25,
        ),
        WeightEstimate(
            ingredient="1 tsp. sugar",
            weight_calculation="1 teaspoon = 5 g, 1 * 5 g = 5 g = 0.005 kg",
            weight_in_kg=0.005,
        ),
        WeightEstimate(
            ingredient="1 organic lemon",
            weight_calculation="1 lemon = 85 g, 1 * 85 g = 85 g = 0.085 kg",
            weight_in_kg=0.085,
        ),
        WeightEstimate(
            ingredient="3 teaspoons salt",
            weight_calculation="1 tsp. = 5 g, 3 * 5 g = 15 g = 0.015 kg",
            weight_in_kg=0.015,
        ),
        WeightEstimate(
            ingredient="2 tbsp. spices",
            weight_calculation="1 tbsp. = 15 g, 2 * 15 g = 30 g = 0.030 kg",
            weight_in_kg=0.03,
        ),
        WeightEstimate(
            ingredient="pepper",
            weight_calculation="Amount of pepper not specified. LLM estimate is: 1 serving = 0.005 kg, 1 * 0.005 kg = 0.005 kg",
            weight_in_kg=0.005,
        ),
        WeightEstimate(
            ingredient="2 large potatoes",
            weight_calculation="1 large potato = 300 g, 2 * 300 g = 600 g = 0.6 kg",
            weight_in_kg=0.6,
        ),
        WeightEstimate(
            ingredient="1 bunch asparagus",
            weight_calculation="1 bunch asparagus = 500 g, 1 * 500 g = 500 g = 0.500 kg",
            weight_in_kg=0.5,
        ),
        WeightEstimate(
            ingredient="1 duck, ca. 2 kg",
            weight_calculation="1 duck, ca. 2 kg = 2000 g, 1 * 2000 g = 2000 g = 2.0 kg",
            weight_in_kg=2.0,
        ),
        WeightEstimate(
            ingredient="Rice for serving",
            weight_calculation="Amount of ingredient not specified, LLM estimate is: 1 serving = 0.125 kg, 4 servings * 0.125 kg = 0.5 kg",
            weight_in_kg=0.5,
        ),
    ]
)

ANSWER_EXAMPLE = ANSWER_EXAMPLE_OBJ.model_dump_json(indent=2)

WEIGHT_CONVERSION_TEMPLATE_EXPLANATION = "<ingredient name> = <weight in grams>, <amount> * <weight in grams> = <total weight in grams> = <total weight in kg>"
INGREDIENT_NOT_FOUND_TEMPLATE = f"Ingredient not found in general weights. LLM estimate is: {WEIGHT_CONVERSION_TEMPLATE_EXPLANATION}."
AMOUNT_NOT_SPECIFIED_TEMPLATE = "Amount of <ingredient> not specified. LLM estimate is: <ingredient name> per serving = <weight in kg>, <number of servings> * <weight in kg> = <total weight in kg>."

WEIGHT_EST_SYSTEM_PROMPT = """
Given a list of ingredients in English or Danish, estimate the weights in kilogram for each ingredient.
Explain your reasoning for the estimation of weights.

The following general weights can be used for estimation:
{recalculations}

**Instructions:**
1. If ingredient has amount and weight specified, convert the weight to kilogram/kg by following the template for 'weight_calculation':
    '{weight_conversion_template}'.
2. If an ingredient is not found in the list of general weights, try to give your best estimate
    of the weight in kilogram/kg of the ingredient and follow the template for 'weight_calculation':
    '{ingredient_not_found_template}'.
3. If the amount of the ingredient is unspecific, then provide an estimate of the weight in kg given the number of servings and follow the template for 'weight_calculation':
    '{amount_not_specified_template}'.
    - Example: 'Serving with rice' depends on the number of servings the ingredient list implies.
4. Your estimate must always be a python float. Therefore, you must not provide any intervals nor set the weight to None if you have calculated an estimate.
5. **IMPORTANT:** Do not alter the name of the ingredient in your response. The ingredient name must be exactly the same as provided in the input.

Input is given after "Ingredients:"

The number of servings is given as a hint to estimate the weight of the ingredients
BUT if it says "Estimate" then you should estimate the weight of the ingredients without the number of servings.
"""

WEIGHT_EST_EXAMPLE_HUMAN_PROMPT = """Ingredients:
{input_example}
The number of servings is 4.

Answer:"""

WEIGHT_EST_EXAMPLE_AI_PROMPT = """{answer_example}"""


def get_weight_est_prompt(language: Languages) -> ChatPromptTemplate:
    """Return weight estimation prompt with examples for the given language."""
    input_example = EN_INPUT_EXAMPLE if language == Languages.English else DA_INPUT_EXAMPLE
    return ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(WEIGHT_EST_SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(WEIGHT_EST_EXAMPLE_HUMAN_PROMPT),
            AIMessagePromptTemplate.from_template(WEIGHT_EST_EXAMPLE_AI_PROMPT),
            HumanMessagePromptTemplate.from_template(
                "Ingredients:\n{input}. \nThe number of servings is {servings}"
            ),
        ],
        input_variables=["input", "servings"],
        partial_variables={
            "recalculations": EN_WEIGHT_RECALCULATIONS,
            "input_example": input_example,
            "answer_example": ANSWER_EXAMPLE,
            "weight_conversion_template": WEIGHT_CONVERSION_TEMPLATE_EXPLANATION,
            "ingredient_not_found_template": INGREDIENT_NOT_FOUND_TEMPLATE,
            "amount_not_specified_template": AMOUNT_NOT_SPECIFIED_TEMPLATE,
        },
    )
