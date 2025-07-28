import re
from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from food_co2_estimator.data.vector_store.vector_store import get_vector_store
from food_co2_estimator.language.detector import Languages

MANUAL_MATCHING_EXCEPTIONS = {
    "oksekød": "oksekød, gennemsnitligt",  # Beef must match to average unless specified
}

# List of number words to recognize spelled-out quantities
NUMBER_WORDS = [
    # English number words
    "one",
    "en",
    "two",
    "to",
    "three",
    "tre",
    "four",
    "fire",
    "five",
    "fem",
    "six",
    "seks",
    "seven",
    "syv",
    "eight",
    "otte",
    "nine",
    "ni",
    "ten",
    "ti",
    "eleven",
    "elleve",
    "twelve",
    "tolv",
    "half",
    "halv",
    "quarter",
    "kvart",
]

# List of units, sorted by length in decreasing order to match longer units first
INGREDIENT_UNITS = sorted(
    [
        # Weight Units
        "milligram",  # en/da
        "milligrams",  # en plural
        "gram",  # en/da
        "grams",  # en plural
        "kilogram",  # en/da
        "kilograms",  # en plural
        "ounce",  # en/da (no common da translation)
        "ounces",  # en plural
        "pound",
        "pund",
        "pounds",  # en plural
        "mg",
        "g",
        "kg",
        "oz",
        "lb",
        "lbs",
        # Volume Units
        "milliliter",  # en/da
        "milliliters",  # en plural
        "deciliter",  # en/da
        "deciliters",  # en plural
        "liter",  # en/da
        "liters",  # en plural
        "litre",  # en alt
        "litres",  # en alt plural
        "cup",
        "kop",
        "cups",  # en plural
        "tablespoon",
        "spiseske",
        "tablespoons",  # en plural
        "teaspoon",
        "teske",
        "teaspoons",  # en plural
        "pint",  # en/da
        "pints",  # en plural
        "quart",  # en/da
        "quarts",  # en plural
        "gallon",  # en/da
        "gallons",  # en plural
        "ml",
        "l",
        "dl",
        "tbsp",
        "spsk",
        "tbsps",
        "tsp",
        "tsk",
        # Danish abbreviations
        "stk",
        "stks",
        "ds",
        "dåse",
        "dåser",
        # Miscellaneous Units
        "package",
        "pakke",
        "packages",
        "pakker",
        "bunch",
        "bundt",
        "bunches",
        "bundter",
        "pinch",
        "nip",
        "pinches",  # en plural
        "clove",
        "fed",
        "cloves",  # en plural
        "slice",
        "skive",
        "slices",
        "skiver",
        "bottle",
        "flaske",
        "bottles",
        "flasker",
        "piece",
        "stykke",
        "pieces",
        "stykker",
        "stick",
        "stang",
        "sticks",
        "stænger",
        "pkg",
        "pkgs",
        "dozen",
        "dusine",
        "jar",
        "glas",
        "can",  # en/da
        "cm",  # en/da
        "drop",
        "dråbe",
        "drops",
        "dråber",
        "large",
        "stor",
        "small",
        "lille",
        "medium",
        "mellem",
        "soft-boiled",
        "smilende",
        "portion",
        # Short Units
        "t",
        "c",
    ],
    key=len,
    reverse=True,
)

FILLER_WORDS = [
    # English and Danish filler words, paired
    "a",
    "en",
    "about",
    "omkring",
    "additional",
    "ekstra",
    "all",
    "alle",
    "an",
    "and",
    "og",
    "any",
    "enhver",
    "approximately",
    "ca",
    "around",
    "at",
    "ved",
    "each",
    "hver",
    "enough",
    "nok",
    "extra",
    "few",
    "få",
    "for",
    "fresh",
    "frisk",
    "full",
    "fuld",
    "handful",
    "håndfuld",
    "just",
    "bare",
    "large",
    "stor",
    "little",
    "lille",
    "medium",
    "mellem",
    "more",
    "mere",
    "nearly",
    "næsten",
    "of",
    "af",
    "or",
    "eller",
    "other",
    "anden",
    "per",
    "piece",
    "stykke",
    "pinch",
    "nip",
    "plus",
    "portion",
    "roughly",
    "omtrent",
    "serving",
    "several",
    "flere",
    "small",
    "some",
    "nogle",
    "tablespoon",
    "spiseske",
    "teaspoon",
    "teske",
    "the",
    "den",
    "to",
    "til",
    "whole",
    "hel",
    "with",
    "med",
    "warm",
    "varm",
    "hot",
    "juice",
    "saften",
    "saft",
    "saften af",
    "juice of",
    "finthakkede",
    "finthakket",
    "finely chopped",
    "finely-chopped",
    "håndfuld",
    "håndfulde",
    "handfuls",
    "håndfulde af",
    # Danish-only words (if any)
    "store",
    "små",
    "styk",
]


def get_clean_regex():
    """
    Removes quantities, units, and the word 'of' from the beginning of an ingredient string.

    Returns:
        Pattern object: Compiled regular expression pattern.
    """

    # Escape any units that might have regex special characters
    escaped_units = [re.escape(unit) for unit in INGREDIENT_UNITS]

    # Join the units with '|' to create the units part of the regex
    units_pattern = r"(?:" + "|".join(escaped_units) + r")\.?"

    # Define the regex pattern
    pattern = r"""
        ^\s*                                      # Leading whitespace
        (?:                                       # Non-capturing group to match quantities and units
            (?:                                   # Non-capturing group for quantity with optional unit
                (?:
                    \d+(?:[\/\-]\d+)?             # Numbers with optional fraction or range
                    | \d*\.\d+                    # Decimal numbers
                    | \b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|en|to|tre|fire|fem|seks|syv|otte|ni|ti|elleve|tolv)\b  # Number words (EN+DA)
                )
                \s*                               # Optional whitespace
                (?:{units})?                      # Optional units
                \s*                               # Optional whitespace
            )
            |                                     # OR
            (?:{units})                           # Units without preceding quantities
        )+                                        # One or more quantities or units
        (?:of\b\s*)?                              # Optional 'of' followed by optional whitespace
    """.format(units=units_pattern)

    # Compile the regex pattern with verbose and ignore case flags
    regex = re.compile(pattern, re.IGNORECASE | re.VERBOSE)

    return regex


def get_emission_retriever(
    *, k: int = 10, language: Languages, **kwargs
) -> VectorStoreRetriever:
    vector_store = get_vector_store(language)
    return vector_store.as_retriever(k=k, **kwargs)


def parse_retriever_output(documents: List[Document]):
    results = {}
    for document in documents:
        metadata = document.metadata
        if "Total kg CO2e/kg" in metadata:
            # Extract and round the emission value.
            try:
                emission = float(metadata["Total kg CO2e/kg"])
                emission_rounded = round(emission, 1)
            except (ValueError, TypeError):
                emission_rounded = None

            # Extract the database id if it exists.
            ID_Ra = metadata.get("ID_Ra", None)

            # Instead of mapping to a string, we now map to a dictionary.
            results[document.page_content] = {
                "emission": f"{emission_rounded} kg CO2e / kg"
                if emission_rounded is not None
                else "none",
                "id": ID_Ra,
            }
    return results


def get_emission_retriever_chain(
    k: int = 5, language: Languages = Languages.English, **kwargs
):
    retriever = get_emission_retriever(k=k, language=language, **kwargs)
    return retriever | parse_retriever_output


async def batch_emission_retriever(inputs: List[str], language: Languages):
    retriever_chain = get_emission_retriever_chain(language=language)
    cleaned_inputs = clean_ingredient_list(inputs)
    cleaned_inputs = transform_input_ingredients(cleaned_inputs)
    outputs = await retriever_chain.abatch(cleaned_inputs)
    if len(outputs) != len(cleaned_inputs):
        raise ValueError
    retriever_matches = dict(zip(inputs, outputs))
    return retriever_matches


def transform_input_ingredients(cleaned_inputs: list[str]) -> list[str]:
    return [
        MANUAL_MATCHING_EXCEPTIONS.get(ingredient, ingredient)
        for ingredient in cleaned_inputs
    ]


def remove_quantities(ingredient: str) -> str:
    """Removes quantities recursively from ingredient string."""

    # Basic number patterns
    decimal_pattern = r"\d*(\.|\,)\d+"  # 0.5, .75
    fraction_pattern = r"\d+(?:\/\d+)?"  # 1/2, 3/4

    # Word patterns including single words and connecting symbols
    number_words_pattern = r"\b(?:" + "|".join(NUMBER_WORDS) + r")\b"
    connecting_symbols = (
        r"(?:to\s+|~|\.\.{2,3}|\-)"  # Require at least one whitespace around 'to'
    )

    filler_words = r"\b(?:" + "|".join(FILLER_WORDS) + r")\b(?:\s+|\-)"

    # Combined pattern
    quantity_pattern = re.compile(
        r"^\s*"  # Start of string and whitespace
        r"(?:"  # Start non-capturing group
        f"(?:{decimal_pattern})"  # Match decimals
        r"|"
        f"(?:{fraction_pattern})"  # Match fractions
        r"|"
        f"(?:{number_words_pattern})"  # Match number words
        r"|"
        f"(?:{connecting_symbols})"  # Require at least one connecting symbol
        r"|"
        f"(?:{filler_words})"  # Match filler words
        r")",
        re.IGNORECASE,
    )

    # Recursive removal until no match
    if quantity_pattern.match(ingredient):
        removed_quantity = quantity_pattern.sub("", ingredient, count=1).strip()
        return remove_quantities(removed_quantity)
    return ingredient


def remove_units(ingredient: str) -> str:
    """
    Removes units from the beginning of an ingredient string.

    Args:
        ingredient (str): The ingredient string to process.

    Returns:
        str: The ingredient string without leading units.
    """
    # Escape units for regex and join them into a pattern
    escaped_units = [re.escape(unit) for unit in INGREDIENT_UNITS]
    units_pattern_str = (
        r"\b(?:" + "|".join(escaped_units) + r")\b\.?"
    )  # Units as whole words, optional period

    # Create a regex pattern to match units with optional 'of' following them
    units_pattern = re.compile(
        r"^\s*"  # Start of string and optional whitespace
        r"(?:" + units_pattern_str + r")"  # Units
        r"(?:\s+of)?"  # Optional 'of' after units
        r"\s*",  # Optional whitespace after units
        re.IGNORECASE,
    )
    # Remove the units from the ingredient string
    removed_units = units_pattern.sub("", ingredient, count=1).strip()
    if removed_units == "":
        return ingredient
    return removed_units


def clean_ingredient_list(ingredients: List[str]) -> List[str]:
    """
    Removes quantities and units from the beginning of each ingredient string in the list.

    Args:
        ingredients (List[str]): The list of ingredient strings to process.

    Returns:
        List[str]: A new list with cleaned ingredient strings.
    """
    cleaned_ingredients = []
    for ingredient in ingredients:
        ingredient = clean_ingredient(ingredient)
        cleaned_ingredients.append(ingredient)
    return cleaned_ingredients


def clean_ingredient(ingredient):
    # Remove quantities
    ingredient = remove_quantities(ingredient)
    # Remove units
    ingredient = remove_units(ingredient)
    return ingredient.lower()
