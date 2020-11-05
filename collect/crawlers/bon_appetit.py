import json

from bs4 import BeautifulSoup
from collect.crawlers.base import BaseCrawler
from collect.models import ingredient_from_string, Recipe

from api.utils import get_cached, clean_str, clean_tags


class BonAppetit(BaseCrawler):

    domain = "bonappetit"
    to_visit_list_urls = [
        "https://www.epicurious.com/recipes-menus/best-brunch-recipes-relaxing-weekend-breakfast-gallery"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

    def get_recipe(self, url):
        content = get_cached(url)
        if content is None:
            return None
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
        script = soup.find("script", {"type": "application/ld+json"})
        recipe_json = script.contents[0]
        try:
            recipe_json = json.loads(recipe_json)
        except:
            return None

        try:
            title = recipe_json["name"]
            image_urls = [recipe_json["image"]]
        except:
            return None

        ingredient_strings = []
        for i in recipe_json["recipeIngredient"]:
            ingredient = clean_str(i)
            ingredient_strings.append(ingredient)
        ingredients = {
            "ingredients": ingredient_strings,
        }

        i = 0
        steps = {}
        for section in recipe_json["recipeInstructions"]:
            s = section["text"]
            steps[f"steps {i}"] = s.split("\xa0")
            i += 1

        tags = [word.lower() for word in title.split(" ")]
        servings = recipe_json.get("recipeYield", 1)

        recipe = Recipe(
            url=url,
            title=title,
            subtitle="",
            ingredients=ingredients,
            instructions=steps,
            servings=servings,
            tags=clean_tags(tags),
            images=image_urls,
        )
        return recipe

    def get_recipe_urls(self):

        recipe_urls = {}
        i = 1
        while True:
            list_url = f"https://www.bonappetit.com/search/?page={i}"
            content = get_cached(list_url)
            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if href.startswith("/"):
                    href = f"https://www.bonappetit.com{href}"
                if "/recipe/" in href and not recipe_urls.get(href, False):
                    recipe_urls[href] = True
                    yield href
            i += 1
