#!/usr/bin/env python
from crawlers.allrecipes import AllRecipes
from utils import store_recipe


if __name__ == "__main__":
    i = 0
    for recipe in AllRecipes().next_recipe(skip_existing=True):
        i += 1
        if recipe is None:
            if i % 100 == 0:
                print(i, "skipped")
            continue
        print(i, recipe.filename, recipe.title)
        store_recipe(recipe)