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
        "2 stk æg",
        "1 stk gulerod",
        "0.5 dl fløde (13%)",
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
- 1 tsk havsalt
- 2 stk æg
- 1 stk gulerod
- ½ dl fløde 13%
- ½ tsk revet muskatnød
- 1 teskefuld peber
- to spsk olie
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
Act as an expert in extracting recipes from text that understand Danish and English.
Given an unstructured raw text containing a recipe, extract the amount of each ingredient, the number of persons, and the instructions.
The instructions are the description of how you prepare the meal.

Follow all these instructions carefully to extract the ingredients:
**Instructions for extracting the ingredients in the recipe:**
1. If an ingredient amount is provided in fractions, words, or other non-numeric formats, then convert it to a numeric format.
    - Example: "½" to "0.5", "⅓" to "0.33", "a half" to "0.5", "one third" to "0.33", etc.
2. If there is extra information for an ingredient that does not is relevant in explaining the ingredient, then remove it.
    - Example: "1 dl olive oil (for frying)" to "1 dl olive oil".
3. Remove any information that describes how the ingredient should be prepared.
    - Example: "1 onion (chopped)" to "1 onion", "1 kg kartofler, hakkede i små tern" to "1 kg kartofler", "2 medium carrots, diced" to "2 medium carrots".
4. Always use the abbreviation for units of measurements.
    - Example: "deciliter" to "dl", "teaspoon" to "tsp", "tablespoon" to "tbsp", "gram" to "g", "kilogram" to "kg", etc.
5. If an ingredient has a range of amounts, then choose the average amount.
    - Example: "1-2 cloves of garlic" to "1.5 cloves of garlic".
6. If an ingredient line has multiple ingredients, then split them into separate lines.
    - Example: "salt and pepper" to "salt" and "pepper", "1 mozarella and 2 tomatoes" to "1 mozarella" and "2 tomatoes".
7. Transcribe the ingredient exactly as it appears in the text except if other instructions apply.
    - Example. "1 cup of milk" to "1 cup of milk", "2 fed hvidløg" til "2 fed hvidløg".
8. If same ingredient is mentioned multiple times, then include it that many times in the list.
9. List the ingredients in the exact same order as they appear in the text.

**Instructions for extracting the number of persons:**
1. It is very important that you extract the number of persons (i.e. number of servings or "antal personer" in danish) from the text.
2. If number not available in text, then estimate the number of persons from the ingredient list based on the amounts in the ingredients.

**Instructions for extracting the instructions:**
1. If the instructions are available, then it is important that you also extract the instructions!
    - Example for instructions title: "Instructions", "How to make", "Preparation", "Instruktioner", "Fremgangsmåde", etc.
2. If number of persons are not explicitly mentioned in text, then estimate from the amount of ingredients.

**Instruction for handling cases where no recipe is found:**
If no recipe to be found, and then you return an empty ingredients list and null in persons and instructions fields.

You must always follow these instructions to extract the recipe correctly. Any deviation from these instructions will result in an incorrect extraction.
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
