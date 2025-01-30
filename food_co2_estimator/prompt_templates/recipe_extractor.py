from langchain.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from food_co2_estimator.pydantic_models.recipe_extractor import ExtractedRecipe

WEBSITE_RESPONSE_OBJ = ExtractedRecipe(
    ingredients=[
        "500 g torskefilet",
        "1 tsk havsalt",
        "1 tsk peber",
        "2 stk æg",
        "1 stk gulerod",
        "0.5 dl fløde (13%)",
        "2 fede hvidløg",
        "0.5 tsk muskatnød",
        "1 tsk peber",
        "2 spsk olie",
        "4 dl creme fraiche (18%)",
        "4 stk æggeblomme",
        "2 spsk frisk dild",
        "4 spsk frisk persille",
        "1 kop mælk",
        "2 fede hvidløg",
        "0.25 bdt koriander",
        "1 håndfuld frisk basilikum",
        "200 g smør",
    ],
    persons=4,
    instructions=(
        "Forvarm ovnen til 180 grader Celsius. Skær torskefileten i mindre stykker og blend den "
        "sammen med havsalt i en foodprocessor til en fin konsistens. Tilsæt æg, fintrevet gulerod, "
        "fløde, revet muskatnød og peber. Blend igen, indtil massen er jævn. Smør en lille brødform "
        "eller ildfast fad med olie og hæld fiskefarsen i formen. Bag terrinen i ovnen i cirka 25-30 "
        "minutter, eller indtil den er fast og gylden på toppen. I mellemtiden piskes creme fraiche "
        "sammen med æggeblommer, hakket dild og persille. Opvarm saucen forsigtigt i en gryde over lav "
        "varme uden at koge den. Tag fisketerrinen ud af ovnen, lad den køle lidt af, og skær den i "
        "skiver. Server med den cremede sauce."
    ),
)
WEBSITE_RESPONSE = WEBSITE_RESPONSE_OBJ.model_dump_json()


NO_RECIPE_RESPONSE_OBJ = ExtractedRecipe(
    ingredients=[],
    persons=None,
    instructions=None,
)
NO_RECIPE_RESPONSE = NO_RECIPE_RESPONSE_OBJ.model_dump_json()

EXAMPLE_INPUT_1 = """
**Ingredienser**
- 500 g torskefilet, i skiver
- 1 tsk havsalt og 1 tsk peber
- 2 stk æg
- 1 stk gulerod
- ½ dl fløde 13%
- to fede hvidløg
- ½ tsk revet muskatnød
- to spsk olie (til stegning)
- 4 dl creme fraiche 18%
- fire stykker æggeblomme
- 2 spsk frisk dild
- 4 spiseskefulde frisk persille
- 1 kop mælk
- to fede hvidløg
- ¼ bundt koriander
- 1 håndfuld frisk basilikum
- 200 g smør (i små stykker)

**Fremgangsmåde**
Forbered fiskefarsen ved at skære torskefileten i mindre stykker og blend den sammen med havsalt i en foodprocessor til en fin konsistens. Tilsæt de to hele æg, fintrevet gulerod, fløde, muskatnød og peber. Blend igen, indtil ingredienserne er godt blandet og konsistensen er jævn. Smag til med salt og peber efter behov
Forvarm ovnen til 180 grader. Smør en lille brødform eller ildfast fad med lidt olie og hæld fiskefarsen i formen. Glat overfladen ud. Bag terrinen i ovnen i cirka 25-30 minutter, eller indtil den er fast og let gylden på toppen
I en lille skål piskes creme fraiche sammen med æggeblommerne, hakket dild og persille. Smag til med salt og peber. Opvarm forsigtigt saucen i en lille gryde over lav varme, indtil den er varm, men undgå at koge den for at undgå at æggeblommerne skiller
Tag fisketerrinen ud af ovnen og lad den køle af i formen i et par minutter. Skær terrinen i skiver og anret på tallerkener. Hæld den cremede sauce over eller server den ved siden af
"""


EXAMPLE_INPUT_2 = """
Det er dejligt vejr i dag. Jeg tror jeg vil gå en tur.
"""

SYSTEM_PROMPT = """
You are an expert in extracting recipe data from unstructured text in Danish or English. Your task is to identify and extract:

1. Ingredients (with amounts in numeric format and standardized units)
2. Number of persons (servings)
3. Instructions (how to prepare the meal)

Follow the detailed instructions below carefully. Any deviation from them will result in an incorrect extraction.

--------------------------------
1. Extracting the Ingredients
--------------------------------
1. Numeric Amounts
   - Convert fractions or word-based quantities into decimal form.
     Examples:
       - ½ → 0.5
       - ⅓ → 0.33
       - a half → 0.5
       - one third → 0.33

2. Remove Irrelevant Details
   - Omit any text in parentheses or after commas that does not describe the ingredient itself.
     Example: "1 dl olive oil (for frying)" → "1 dl olive oil"
     Example: "1 onion, chopped" → "1 onion"

3. Standardize Units
   - Convert measurement units to abbreviations.
     Examples:
       - deciliter → dl
       - teaspoon → tsp
       - tablespoon → tbsp
       - gram → g
       - kilogram → kg

4. Handle Ranges
   - For ranges (e.g., "1–2 cloves of garlic"), use the average.
     Example: "1–2 cloves of garlic" → "1.5 cloves of garlic"

5. Split Multiple Ingredients
   - If a line contains multiple ingredients, split them into separate lines.
     Example: "salt and pepper" → "salt" and "pepper"

6. Preserve Original Naming
   - Keep the original words for each ingredient (unless modified by the above rules).
     Example: "2 fed hvidløg" remains "2 fed hvidløg"

7. Respect Order and Repetitions
   - List ingredients in the exact order they appear in the text.
   - If the same ingredient appears multiple times, list it each time it appears.

-------------------------------------
2. Extracting the Number of Persons
-------------------------------------
1. Look for Explicit Mentions
   - If the text explicitly states a number of persons or servings, extract that number.

2. Estimation if Not Explicit
   - If the text does not explicitly mention a number of persons, estimate it based on the total amounts of ingredients provided.

--------------------------------
3. Extracting the Instructions
--------------------------------
1. Identify Instruction Sections
   - Look for sections titled “Instructions,” “How to make,” “Preparation,” “Fremgangsmåde,” “Instruktioner,” or similar.

2. Extract the Preparation Steps
   - Include all text that explains how to prepare or cook the dish.

3. If No Instructions
   - If you cannot find instructions, return null for instructions.

--------------------------------------
4. If No Recipe Is Found in the Text
--------------------------------------
- If no recognizable recipe is found:
  - Return an empty list for ingredients: []
  - Return null for both the number of persons and the instructions

Remember: You must follow these rules exactly to ensure accurate extraction.
"""


messages = [
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template("{example_input_1}"),
    AIMessagePromptTemplate.from_template("{website_response}"),
    HumanMessagePromptTemplate.from_template("{example_input_2}"),
    AIMessagePromptTemplate.from_template("{no_recipe_response}"),
    HumanMessagePromptTemplate.from_template("{input}"),
]

RECIPE_EXTRACTOR_PROMPT = ChatPromptTemplate(
    messages=messages,
    input_variables=["input"],
    partial_variables={
        "example_input_1": EXAMPLE_INPUT_1,
        "website_response": WEBSITE_RESPONSE,
        "example_input_2": EXAMPLE_INPUT_2,
        "no_recipe_response": NO_RECIPE_RESPONSE,
    },
)
