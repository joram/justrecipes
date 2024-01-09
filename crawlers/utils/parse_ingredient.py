import re

from bs4 import BeautifulSoup
from parse_ingredients import Ingredient as ParsedIngredient
from parse_ingredients import parse_ingredient as _parse_ingredient

from fda import convert_ingredient_using_golden_file
from recipes.models import Ingredient


def _clean_ingredient(ingredient_string):
    ingredient_string = convert_ingredient_using_golden_file(ingredient_string)

    if "</" in ingredient_string:
        soup = BeautifulSoup(ingredient_string, 'html.parser')
        ingredient_string = soup.get_text()

    ingredient_string = ingredient_string.lower()
    ingredient_string = re.sub(r'\(.*\)', '', ingredient_string)

    if " plus " in ingredient_string:
        ingredient_string = ingredient_string.split(" plus ")[0]

    for unit in ["cups", "cup", "tablespoons", "ounce", "ounces", "pound", "pounds"]:
        bad_s = f" {unit}/"
        if bad_s in ingredient_string:
            ingredient_string = ingredient_string.split(bad_s)[1]
        if f"-{unit}" in ingredient_string:
            ingredient_string = ingredient_string.replace(f"-{unit}", f" {unit}")

    for bad_word in ["optional", "to taste", "for serving"]:
        ingredient_string = ingredient_string.replace(bad_word, "")
    if "</" in ingredient_string:
        soup = BeautifulSoup(ingredient_string, 'html.parser')
        ingredient_string = soup.get_text()
    ingredient_string = ingredient_string.strip()
    ingredient_string = ingredient_string.replace("pinch", "a 1/4 tsp")

    substitute_words = {
        "¼": "1/4",
        "½": "1/2",
        "¾": "3/4",
        "⅓": "1/3",
        "⅔": "2/3",
        "⅛": "1/8",
        "⅜": "3/8",
        "⅝": "5/8",
        "⅞": "7/8",
        "⅕": "1/5",
        "⅖": "2/5",
        "⅗": "3/5",
        "⅘": "4/5",
        " ": " ",
    }
    for word, replacement in substitute_words.items():
        ingredient_string = ingredient_string.replace(word, replacement)

    if " or " in ingredient_string:
        ingredient_string = ingredient_string.split(" or ")[0]

    while "  " in ingredient_string:
        ingredient_string = ingredient_string.replace("  ", " ")
    ingredient_string = ingredient_string.rstrip(",")

    return ingredient_string

def parse_ingredient(ingredient_string):
    original_ingredient_string = ingredient_string
    ingredient_string = _clean_ingredient(ingredient_string)
    try:
        parsed_ingredient = _parse_ingredient(ingredient_string)
    except Exception as e:
        parsed_ingredient = ParsedIngredient(
            name=ingredient_string,
            quantity=1,
            unit="",
            comment="",
            original_string=original_ingredient_string,
        )

    return Ingredient(
        name=parsed_ingredient.name,
        amount=parsed_ingredient.quantity,
        unit=parsed_ingredient.unit,
        comment=parsed_ingredient.comment,
        nutrition_infos=[],
        original_string=original_ingredient_string,
    )