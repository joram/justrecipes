#!/usr/bin/env python

from api.utils import store_recipe, store_tags, store_recipes, load_recipes
from collect.crawlers.allrecipes import AllRecipes
from collect.crawlers.aseasyasapplepie import AsEasyAsApplePie
from collect.crawlers.bon_appetit import BonAppetit
from collect.crawlers.epicurious import Epicurious
from collect.models import recipe_id, Recipe

recipes = load_recipes()


def build_tags():
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


def recipes_generator(start_at=0, load_existing=False):
    crawlers = [
        Epicurious(),
        AllRecipes(),
        BonAppetit(),
        AsEasyAsApplePie(),
    ]
    generators = {}

    for i in range(0, 100000000):
        crawler = crawlers[i % len(crawlers)]
        if crawler.domain not in generators:
            generators[crawler.domain] = crawler.get_recipe_urls()
        try:
            url = generators[crawler.domain].__next__()
        except:
            continue

        if i < start_at:
            if i % 100 == 0:
                print(f"{i}/{start_at} skipped")
            continue

        id = recipe_id(url)
        if id in recipes:
            yield Recipe.from_json(recipes[id]), True
            continue

        recipe = crawler.get_recipe(url)

        if recipe is None:
            continue
        yield recipe, False


def crawl():
    tags = []
    i = 0
    for recipe, cached in recipes_generator(start_at=0, load_existing=True):
        recipes[recipe.id] = recipe.json()
        recipe.store_images()

        if i % 100 == 0 and not cached:
            store_recipes(recipes)
            tags = build_tags()
            store_tags(tags)

        print(f"visited:{i} recipes:{len(recipes)} tags:{len(tags)} imgs:{len(recipe.images)} {recipe.domain}\t {recipe.filename} recipe:{recipe.title}")
        store_recipe(recipe, overwrite=True)
        i += 1


if __name__ == "__main__":
    crawl()
