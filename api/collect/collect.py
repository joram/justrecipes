#!/usr/bin/env python
import time

from crawlers.allrecipes import AllRecipes
from crawlers.aseasyasapplepie import AsEasyAsApplePie
from crawlers.epicurious import Epicurious
from utils import store_recipe, store_tags, store_recipes, load_recipes


def build_tags(recipes):
    results = {}
    for recipe in recipes.values():
        for tag in recipe.get("tags", []):
            if tag not in results:
                results[tag] = {
                    "count": 0,
                    "tag": tag
                }
            results[tag]["count"] += 1

    tags = list(results.values())
    store_tags(tags)
    return tags


def crawl():
    tags = []
    recipes = load_recipes()
    crawlers = [
        (Epicurious(), Epicurious().next_recipe(skip_existing=False)),
        (AllRecipes(), AllRecipes().next_recipe(skip_existing=False)),
        # AsEasyAsApplePie().next_recipe(skip_existing=False)),
    ]

    for i in range(0, 100000000):
        crawler, generator = crawlers[i % len(crawlers)]
        recipe = generator.__next__()

        if recipe is None:
            if i % 100 == 0:
                print(i, "skipped")
            continue

        recipes[recipe.id] = recipe.json()
        recipe.store_images()
        if i % 100 == 0:
            store_recipes(recipes)
            tags = build_tags(recipes)
            store_tags(tags)

        print(f"{crawler.domain}:\t visited {i} recipes, stored {len(recipes)} recipes, and {len(tags)} tags\t\timgs: {len(recipe.images)} recipe: {recipe.title}")
        store_recipe(recipe, overwrite=True)


if __name__ == "__main__":
    crawl()
