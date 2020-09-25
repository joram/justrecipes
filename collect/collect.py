#!/usr/bin/env python
from crawlers.allrecipes import AllRecipes
from utils import store_recipe


if __name__ == "__main__":
    for recipe in AllRecipes().next_recipe():
        print(recipe.filename, recipe.title)
        store_recipe(recipe)
