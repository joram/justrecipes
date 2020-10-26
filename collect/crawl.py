#!/usr/bin/env python
import sqlalchemy

from collect.crawlers.allrecipes import AllRecipes
from collect.crawlers.aseasyasapplepie import AsEasyAsApplePie
from collect.crawlers.bon_appetit import BonAppetit
from collect.crawlers.epicurious import Epicurious
from collect.models import recipe_id, Recipe
from db.recipe import Recipe as DBRecipe, Tag, RecipeTag, Session


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

        if not load_existing:
            session = Session()
            qs = session.query(DBRecipe).filter(DBRecipe.pub_id == recipe_id(url))
            if len(qs.all()) != 0:
                yield qs.all()[0], True
                continue

        recipe = crawler.get_recipe(url)

        if recipe is None:
            continue
        yield recipe, False


def crawl():
    i = 0
    for recipe, cached in recipes_generator(start_at=0, load_existing=False):
        if type(recipe.images) == list:
            recipe.images = {
                "originals": recipe.images,
                "x512": [
                    f"https://s3-us-west-2.amazonaws.com/assets.recipes.oram.ca/images/{recipe.id}.{i}.512.square.jpg" for
                    i in range(0, len(recipe.images))],
            }
        if not cached:
            db_recipe = DBRecipe.from_json(recipe)
            db_recipe.save()
        print(f"visited:{i} cached:{'T' if cached else 'F'}\tdomain:{recipe.domain}\t {recipe.filename} recipe:{recipe.title}")
        i += 1


if __name__ == "__main__":
    crawl()
