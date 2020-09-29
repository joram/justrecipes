import os

from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler
from models import ingredient_from_string, Recipe
from utils import get_cached, clean_str, recipe_exists


class Epicurious(BaseCrawler):

    domain = "epicurious"
    to_visit_list_urls = [
        "https://www.epicurious.com/recipes-menus/best-brunch-recipes-relaxing-weekend-breakfast-gallery"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

    def get_recipe(self, url):
        content = get_cached(url)
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

        title = soup.find("h1", {"itemprop": "name"})
        title = str(title.text)

        ingredients = {}
        ingredient_groups = soup.findAll("ol", {"class": "ingredient-groups"})
        for group in ingredient_groups:
            group_title = soup.find("strong").text
            group_ingredients = []
            lis = group.findAll("li", {"class": "ingredient"})
            for li in lis:
                s = clean_str(li.text)
                i = ingredient_from_string(s)
                if i is not None:
                    group_ingredients.append(i)
            ingredients[group_title] = group_ingredients

        steps = {}
        preparation_groups = soup.findAll("ol", {"class": "preparation-groups"})
        for group in preparation_groups:
            group_title = soup.find("strong").text
            group_steps = []
            lis = group.findAll("li", {"class": "preparation-step"})
            for li in lis:
                step = clean_str(li.text)
                group_steps.append(step)
            steps[group_title] = group_steps

        dt = soup.find("dl", {"class": "tags"})
        dts = dt.findAll("dt")
        tags = [str(dt.text) for dt in dts]

        servings = soup.find("dd", {"class": "yield"}).text

        div = soup.find("div", {"class": "recipe-image"})
        img = div.find("meta", {"itemprop": "image"})
        image_url = img.attrs['content']
        print(image_url)
        recipe = Recipe(
            url=url,
            title=title,
            subtitle="",
            ingredients=ingredients,
            instructions=steps,
            servings=servings,
            category=[],
            tags=tags,
            images=[image_url],
        )
        return recipe

    def get_recipe_urls(self):

        recipe_urls = {}
        i = 1
        while True:
            list_url = f"https://www.epicurious.com/search?page={i}"
            content = get_cached(list_url)
            if "DON'T CRY!" in str(content):
                break
            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if href.startswith("/"):
                    href = f"https://www.epicurious.com{href}"
                if "/recipes/food/views/" in href and not recipe_urls.get(href, False):
                    recipe_urls[href] = True
                    yield href
            i += 1