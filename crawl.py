#!/usr/bin/env python

from crawlers import AllRecipes, BonAppetit, Epicurious, NYTimes, FoodNetwork
from db.recipe import Recipe as DBRecipe, Tag, Session


def recipes_generator(load_existing=False):
    crawlers = [
        Epicurious(),
        AllRecipes(),
        BonAppetit(),
        # AsEasyAsApplePie(),
        NYTimes(),
        FoodNetwork(),
    ]

    generators = {}
    for crawler in crawlers:
        if crawler.domain not in generators:
            generators[crawler.domain] = crawler.get_recipe_urls()

    for i in range(0, 100000000):

        # Pick url
        crawler_names = list(generators.keys())
        crawler_names.sort()
        crawler_name = crawler_names[i % len(crawler_names)]
        try:
            url = generators[crawler_name].__next__()
        except StopIteration:
            del generators[crawler_name]
            continue

        # Skip existing
        if not load_existing:
            session = Session()
            qs = session.query(DBRecipe).filter(DBRecipe.pub_id == DBRecipe.get_pub_id(url))
            if len(qs.all()) != 0:
                yield qs.all()[0], True
                continue

        # Get recipe
        recipe = crawler.get_recipe(url)
        if recipe is None:
            continue

        yield recipe, False


def crawl():
    print("starting crawl")
    i = 0
    for recipe, cached in recipes_generator(load_existing=False):
        print(f"visited:{i} cached:{'T' if cached else 'F'} pub_id:{recipe.pub_id} \tdomain:{recipe.domain}\t recipe:{recipe.title}")
        if not cached:
            recipe.save()
        i += 1


def update_tag_count():
    session = Session()
    for tag in session.query(Tag).all():
        tag.count = len(tag.recipe_pub_ids())
        print(tag)
        session.add(tag)
        session.commit()


if __name__ == "__main__":
    crawl()
