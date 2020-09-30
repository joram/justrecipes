#!/usr/bin/env python
import time

from crawlers.allrecipes import AllRecipes
from crawlers.aseasyasapplepie import AsEasyAsApplePie
from crawlers.epicurious import Epicurious
from utils import store_recipe, store_tags, store_recipes


def build_tags(recipes):
    results = {}
    for recipe in recipes.values():
        for tag in recipe.get("tags", []):
            tag = tag.lower()
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
    recipes = {}
    for crawler in [
        Epicurious(),
        AllRecipes(),
        AsEasyAsApplePie(),
    ]:
        i = 0
        for recipe in crawler.next_recipe(skip_existing=False):
            i += 1
            if recipe is None:
                if i % 100 == 0:
                    print(i, "skipped")
                continue

            recipes[recipe.id] = recipe.json()
            if i % 100 == 0:
                print(
                    crawler.domain,
                    i,
                    "\t",
                    recipe.title,
                )

                store_recipes(recipes)
                tags = build_tags(recipes)
                store_tags(tags)
                print(f"stored {len(recipes)} recipes, and {len(tags)} tags")
                time.sleep(1)
            else:
                print(".", end='\r')

            store_recipe(recipe, overwrite=True)


if __name__ == "__main__":
    crawl()
