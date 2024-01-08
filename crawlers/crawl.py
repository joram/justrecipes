#!/usr/bin/env python
import asyncio
import os

from bs4 import BeautifulSoup

from recipes.models import Recipe
from utils.caching import get_cached
from utils.get_schema_data import get_schema_data
from utils.recipe_urls import recipe_urls
from utils.schema_to_recipe import create_recipe


async def recipes_generator():
    i = 0
    async for url, index, total in recipe_urls():
        content = await get_cached(url)
        if content is None:
            print("no content for url: ", url)
            continue
        soup = BeautifulSoup(content, 'html.parser')
        schemas = list(get_schema_data(soup))
        for data in schemas:
            recipe = await create_recipe(data, url)
            if recipe is None:
                continue
            left_s = f"{i} {index}/{total} {recipe.name}"
            space = " " * (100 - len(left_s))
            print(f"{left_s}{space}{url}")
            yield recipe
            i += 1


def save_recipe(recipe: Recipe):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(current_dir, f"../recipes/data/{recipe.name}.json")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w") as f:
        f.write(recipe.model_dump_json(indent=2))


async def crawl():
    print("starting crawl")
    async for recipe in recipes_generator():
        save_recipe(recipe)


if __name__ == "__main__":
    asyncio.run(crawl())