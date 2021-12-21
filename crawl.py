#!/usr/bin/env python

from crawlers import AllRecipes, BonAppetit, Epicurious, NYTimes, FoodNetwork
from db.recipe import Recipe as DBRecipe, Tag, Session


def recipes_generator(start_at=0, load_existing=False):
    crawlers = [
        Epicurious(),
        AllRecipes(),
        BonAppetit(),
        # AsEasyAsApplePie(),
        NYTimes(),
        FoodNetwork(),
    ]
    generators = {}

    for i in range(0, 100000000):
        crawler = crawlers[i % len(crawlers)]
        if crawler.domain not in generators:
            generators[crawler.domain] = crawler.get_recipe_urls()
        url = generators[crawler.domain].__next__()
        if i < start_at:
            if i % 100 == 0:
                print(f"{i}/{start_at} skipped")
            continue

        if not load_existing:
            session = Session()
            qs = session.query(DBRecipe).filter(DBRecipe.pub_id == DBRecipe.get_pub_id(url))
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
        recipe.save()
        yield recipe, False


def crawl():
    print("starting crawl")
    i = 0
    for recipe, cached in recipes_generator(start_at=0, load_existing=False):
        print(f"visited:{i} cached:{'T' if cached else 'F'} pub_id:{recipe.pub_id} \tdomain:{recipe.domain}\t recipe:{recipe.title}")

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
