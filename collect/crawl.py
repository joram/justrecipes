#!/usr/bin/env python
import atexit

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

        def clean(tag):
            tag = tag.replace("\"", "")
            tag = tag.replace(",", "")
            tag = tag.replace("(", "")
            tag = tag.replace(")", "")
            if len(tag) == 0:
                return None
            if tag[0] == "&":
                return None
            if tag[0] == "1":
                return None
            if tag[0] == "2":
                return None
            if tag[0] == "3":
                return None
            return tag

        recipe.tags = [clean(tag) for tag in recipe.tags if clean(tag) is not None]

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
        print(f"visited:{i} cached:{'T' if cached else 'F'}\tdomain:{recipe.domain}\t recipe:{recipe.title}")

        i += 1


def update_tag_count():
    session = Session()
    for tag in session.query(Tag).all():
        tag.count = len(tag.recipe_pub_ids())
        print(tag)
        session.add(tag)
        session.commit()


if __name__ == "__main__":
    atexit.register(update_tag_count)
    crawl()
