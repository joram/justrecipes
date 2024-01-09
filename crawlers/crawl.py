#!/usr/bin/env python
import asyncio
import os
from typing import Optional

from bs4 import BeautifulSoup

from recipes.models import Recipe
from utils.caching import get_cached
from utils.get_schema_data import get_schema_data
from utils.recipe_urls import recipe_urls
from utils.schema_to_recipe import create_recipe


def recipes_generator(skip=0):
    def _print(i, index, total, recipe: Optional[Recipe], url: str):
        recipe_name = recipe.name if recipe else "skipped"
        left_s = f"{i} {index}/{total} {recipe_name}"
        space = " " * (100 - len(left_s))
        print(f"{left_s}{space}{url}")


    i = 0
    for url, index, total in recipe_urls():
        if i < skip:
            i += 1
            _print(i, index, total, None, url)
            continue
        content = get_cached(url)
        if content is None:
            print("no content for url: ", url)
            continue
        soup = BeautifulSoup(content, 'html.parser')
        schemas = list(get_schema_data(soup))
        for data in schemas:
            recipe = create_recipe(data, url)
            if recipe is None:
                continue
            _print(i, index, total, recipe, url)
            yield recipe
            i += 1


def save_recipe(recipe: Recipe):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(current_dir, f"../recipes/data/{recipe.name}.json")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    new_content = recipe.model_dump_json(indent=2)
    if os.path.exists(filepath):
        original_content = open(filepath, "r").read()
        if new_content == original_content:
            return

    with open(filepath, "w") as f:
        f.write(new_content)


def crawl():
    print("starting crawl")
    for recipe in recipes_generator(skip=3000):
        save_recipe(recipe)


if __name__ == "__main__":
    crawl()