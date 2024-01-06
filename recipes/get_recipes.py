#!/usr/bin/env python3
import os
from typing import Generator

from .models import Recipe


# a generator function that returns the recipes stored in the data directory
# it is a generator to avoid loading all the recipes in memory at once
def get_recipes() -> Generator[Recipe, None, None]:
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(current_dir, f"./data/")
    os.makedirs(os.path.dirname(data_dir), exist_ok=True)

    for file_name in os.listdir(data_dir):
        with open(f"{data_dir}/{file_name}") as f:
            content = f.read()
            yield Recipe.model_validate_json(content)


if __name__ == "__main__":
    for recipe in get_recipes():
        print(recipe.name)
        print(recipe.categories)
        print(recipe.servings)
        print(recipe.minutes)
        print(recipe.source_url)
        print(recipe.image_urls)
        print(recipe.ingredients)
        print(recipe.instructions)
        print(recipe.notes)
        print(recipe.nutrition_infos)
        print()
