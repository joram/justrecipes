#!/usr/bin/env python
import os

import requests
from bs4 import BeautifulSoup
from quantulum3 import parser
from fractions import Fraction

from models import Ingredient, Recipe


def _cache_path(resource):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../cache")
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

    resource = resource.rstrip("/")
    if not resource.endswith("/index.html"):
        resource = f"{resource}/index.html"

    path = os.path.join(
        os.path.abspath(cache_path),
        resource.lstrip("https://"),
    )

    resource_dir = os.path.dirname(path)
    if not os.path.exists(resource_dir):
        os.makedirs(resource_dir)
    return path


def get_cached(url):
    path = _cache_path(url)
    if os.path.exists(path):
        with open(path, "rb") as f:
            content = f.read()
            return content

    with open(path, "wb") as f:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response.status_code)

        f.write(response.content)
        return response.content


def clean_str(s):
    s = str(s)
    s = s.replace("½", "1/2")
    s = s.replace("¼", "1/4")
    s = str(s).lstrip(" \\n\n\t").rstrip(" \\n\n\t").replace("  ", " ")
    return s


def ingredient_from_string(s):
    quantums = parser.parse(s)
    qu = quantums[0]

    s = s.replace(qu.to_spoken(), "")
    if str(qu.unit) != "":
        s = s.replace(f"{str(qu.unit)}s", "")
        s = s.replace(str(qu.unit), "")
    s = s.replace(str(Fraction(qu.value)), "")
    s = s.split(", ")[0]
    s = s.split(" - ")[0]
    s = s.lstrip(" ")
    return Ingredient(
        name=s,
        amount=qu.value,
        unit=qu.unit,
    )


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