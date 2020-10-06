#!/usr/bin/env python

from api.utils import store_recipe, store_tags, store_recipes, load_recipes
from collect.crawlers.allrecipes import AllRecipes
from collect.crawlers.aseasyasapplepie import AsEasyAsApplePie
from collect.crawlers.bon_appetit import BonAppetit
from collect.crawlers.epicurious import Epicurious


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


def recipes_generator(start_at=5200, load_existing=False):
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

        # id = recipe_id(url)
        # if recipe_exists(id):
        #     actually_load = False
        #     data = load_recipe_from_file(id)
        #     ingredients = data["ingredients"]
        #     for category in ingredients:
        #         old = ingredients[category]
        #         ingredients[category] = []
        #         for i in old:
        #             i = i.get("original")
        #             if i is None:
        #                 actually_load = True
        #                 break
        #
        #             i = ingredient_from_string(i)
        #
        #             if i is not None:
        #                 ingredients[category].append(i)
        #
        #     if actually_load:
        #         recipe = crawler.get_recipe(url)
        #     else:
        #         recipe = Recipe(
        #             url=data["url"],
        #             title=data["title"],
        #             subtitle="",
        #             servings=1,
        #             ingredients=ingredients,
        #             instructions=data["instructions"],
        #             tags=data["tags"],
        #             images=data["images"],
        #         )
        # else:
        recipe = crawler.get_recipe(url)

        if recipe is None:
            continue
        yield recipe


def crawl():
    tags = []
    recipes = load_recipes()
    i = 0
    for recipe in recipes_generator(start_at=25000, load_existing=True):
        recipes[recipe.id] = recipe.json()
        recipe.store_images()
        if i % 100 == 0:
            store_recipes(recipes)
            tags = build_tags(recipes)
            store_tags(tags)

        print(f"visited:{i} recipes:{len(recipes)} tags:{len(tags)} imgs:{len(recipe.images)} filename:{recipe.filename} recipe:{recipe.title}")
        store_recipe(recipe, overwrite=True)
        i += 1


if __name__ == "__main__":
    crawl()
