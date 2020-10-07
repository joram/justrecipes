#!/usr/bin/env python
import json
import os
import time

from api.utils import load_recipes
from ingredients.parse import Parser

test_content = """
from ingredients.parse import Parser


def test_ingredient():
    parser = Parser()
    actual = parser.parse("{ingredient}")
    expected = {expected}

    assert actual == expected
"""


def _get_practice_ingredients(max_ingredients=None):
    recipes = load_recipes()
    for id in recipes:
        ingredient_dict = recipes[id].get("ingredients", [])
        for ingredient_key in ingredient_dict:
            for ingredient in ingredient_dict[ingredient_key]:
                yield ingredient
                if max_ingredients is not None:
                    max_ingredients -= 1
                    if max_ingredients <= 0:
                        return


def gen_tests():
    p = Parser()
    i = 0
    for ingredient in _get_practice_ingredients():
        filename = f"test_{ingredient.replace(' ', '_').replace('/','slash')}.py"
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
        content = test_content.format(
            ingredient=ingredient,
            expected=json.dumps(p.parse(ingredient), indent=4, sort_keys=True),
        )

        with open(filepath, "w") as f:
            f.write(content)
        print(filepath)
        i += 1
        time.sleep(1)

gen_tests()
