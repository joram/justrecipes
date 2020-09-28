#!/usr/bin/env python

from bs4 import BeautifulSoup
from quantulum3 import load
from quantulum3.classes import Quantity

from crawlers.base import BaseCrawler
from models import ingredient_from_string, Recipe, Ingredient
from utils import get_cached


class AsEasyAsApplePie(BaseCrawler):

    def get_recipe_urls(self):
        recipe_urls = []
        list_urls = [
            "https://aseasyasapplepie.com/tag/cumin/",
            "https://aseasyasapplepie.com/recipe-index/",
        ]
        for url in list_urls:
            content = get_cached(url)
            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]

                if href in recipe_urls:
                    continue

                if not href.startswith("https://aseasyasapplepie.com"):
                    continue

                if href.startswith("https://aseasyasapplepie.com/tag") or href.startswith("https://aseasyasapplepie.com/category"):
                    if href not in list_urls:
                        list_urls.append(href)
                    continue

                page_content = get_cached(href)
                page_soup = BeautifulSoup(page_content.decode("utf-8"), "html.parser")
                special_link = page_soup.findAll("div", {"class": "wprm-recipe-snippets"})
                if len(special_link) > 0:
                    recipe_urls.append(href)
                    yield href

        return []

    def get_recipe(self, url):
        content = get_cached(url)
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

        def _get_span(classname):
            span = li.find("span", {"class": classname})
            if span is None:
                return ""
            return span.text

        div = soup.find("div", {"class": "wprm-recipe-name wprm-color-header"})
        title = div.text

        ingredients = []
        lis = soup.findAll("li", {"class": "wprm-recipe-ingredient"})
        for li in lis:
            amount = _get_span("wprm-recipe-ingredient-amount")
            unit = _get_span("wprm-recipe-ingredient-unit")
            name = _get_span("wprm-recipe-ingredient-name")
            notes = _get_span("wprm-recipe-ingredient-notes")
            ingredient = ingredient_from_string(f"{amount} {unit}")
            if ingredient is None:
                ingredient = Ingredient(
                    name=name,
                    quantity=Quantity(
                        value=1,
                        unit=load.units("en").names["dimensionless"],
                    )
                )
            else:
                ingredient.name = name
                ingredient.notes = notes
            ingredients.append(ingredient)

        instructions = []
        divs = soup.findAll("div", {"class": "wprm-recipe-instruction-text"})
        for div in divs:
            instructions.append(div.text)

        return Recipe(
            url=url,
            title=title,
            subtitle="",
            servings=0,
            ingredients=ingredients,
            instructions=instructions,
        )
