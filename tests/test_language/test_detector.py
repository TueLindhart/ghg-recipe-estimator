import pytest

from food_co2_estimator.language.detector import Languages, detect_language


@pytest.mark.parametrize(
    "ingredients, instructions, expected_language",
    [
        (
            ["eggplant", "cucumber"],
            "Preheat the oven to 180 degrees. Add salt and pepper.",
            Languages.English,
        ),
        (
            ["aubergine", "agurk"],
            "Forvarm ovnen til 180 grader. Tilsæt salt og peber.",
            Languages.Danish,
        ),
        (
            ["berenjena", "pepino"],
            "Precalienta el horno a 180 grados. Añade sal y pimienta.",
            None,
        ),
    ],
    ids=["english", "danish", "spanish"],
)
def test_detect_language(ingredients, instructions, expected_language):
    assert detect_language(instructions, ingredients) == expected_language


def test_empty_recipe_raises_exception():
    with pytest.raises(Exception):
        detect_language(None, [])


@pytest.mark.parametrize(
    "ingredients, instructions, expected_language",
    [
        (
            ["salt", "pepper"],
            "Forvarm ovnen til 180 grader. Dette er en norsk oppskrift.",
            Languages.Danish,
        ),
        (
            ["salt", "pepper"],
            "Förvärm ugnen till 180 grader. Detta är ett svenskt recept.",
            Languages.Danish,
        ),
    ],
    ids=["norwegian", "swedish"],
)
def test_norwegian_and_swedish_as_danish(ingredients, instructions, expected_language):
    assert detect_language(instructions, ingredients) == expected_language


@pytest.mark.parametrize(
    "ingredients, expected_language",
    [
        (
            [
                "500 gram torskefilet",
                "2 stk æg",
                "1 stk gulerod, fintrevet",
                "0.5 tsk revet muskatnød",
                "2 spsk olie",
                "4 dl creme fraiche (18%)",
                "4 stk æggeblomme",
                "2 spsk frisk dild, hakket",
                "4 spsk frisk persille, hakket",
            ],
            Languages.Danish,
        ),
        (
            [
                "500 grams cod fillet",
                "2 eggs",
                "1 carrot, finely grated",
                "0.5 tsp grated nutmeg",
                "2 tbsp oil",
                "4 dl sour cream (18%)",
                "4 egg yolks",
                "2 tbsp fresh dill, chopped",
                "4 tbsp fresh parsley, chopped",
            ],
            Languages.English,
        ),
        (
            [
                "500 gramos de filete de bacalao",
                "2 huevos",
                "1 zanahoria, finamente rallada",
                "0.5 cucharadita de nuez moscada rallada",
                "2 cucharadas de aceite",
                "4 dl de crema agria (18%)",
                "4 yemas de huevo",
                "2 cucharadas de eneldo fresco, picado",
                "4 cucharadas de perejil fresco, picado",
            ],
            None,
        ),
    ],
    ids=["danish", "english", "spanish"],
)
def test_ingredients_no_instructions(ingredients, expected_language):
    assert detect_language(None, ingredients) == expected_language


def test_single_word_ingredients():
    assert detect_language(None, ["agurk", "gulerod", "ærter"]) == Languages.Danish
