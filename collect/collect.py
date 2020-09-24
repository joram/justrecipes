#!/usr/bin/env python

from bs4 import BeautifulSoup
from models import Recipe, ingredient_from_string
from utils import get_cached, clean_str


def get_allrecipes_recipe(url):
    content = get_cached(url)
    soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

    title = soup.find("h1", {"class": "headline"})
    title = str(title.text)

    ingredients = []
    lis = soup.findAll("li", {"class": "ingredients-item"})
    for li in lis:
        s = clean_str(li.text)
        ingredients.append(ingredient_from_string(s))

    steps = []
    divs = soup.findAll("div", {"class": "paragraph"})
    for div in divs:
        step = clean_str(div.text)
        steps.append(step)

    servings = None
    divs = soup.findAll("div", {"class": "recipe-meta-item"})
    for div in divs:
        key = clean_str(div.find("div", {"class":"recipe-meta-item-header"}))
        val = clean_str(div.find("div", {"class":"recipe-meta-item-body"}))
        if key.lower() == "yield:":
            servings = val
            break

    return Recipe(
        title=title,
        subtitle=None,
        ingredients=ingredients,
        instructions=steps,
        servings=servings,
    )


if __name__ == "__main__":

    urls = [
        "https://www.allrecipes.com/recipe/20185/virginas-tuna-salad/",
        "https://www.allrecipes.com/recipe/270527/instant-pot-galbi-korean-style-short-ribs/",
    ]
    for url in urls:
        r = get_allrecipes_recipe(url)
        print(r)
