from enum import StrEnum

from langdetect import detect


class Languages(StrEnum):
    English = "en"
    Danish = "da"
    Norwegian = "no"
    Swedish = "sv"
    Unknown = "unknown"


ALLOWED_LANGUAGE_MISTAKES = [Languages.Norwegian.value, Languages.Swedish.value]


def detect_language(instructions: str | None, ingredients: list[str]) -> Languages:
    language = (
        detect(instructions)
        if instructions is not None
        else detect(", ".join(ingredients))
    )
    if language in ALLOWED_LANGUAGE_MISTAKES:  # Swedish and Norwegian is easy mistakes
        return Languages.Danish

    if language in [lang.value for lang in Languages]:
        return Languages(language)
    return Languages.Unknown
