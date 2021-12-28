import json

import requests
from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler
from utils import get_cached


class AllRecipes(BaseCrawler):
    domain = "allrecipes.com"

    def get_recipe_urls(self):
        recipe_urls = {}
        i = 1
        while True:
            response = get_cached(f"https://www.allrecipes.com/element-api/content-proxy/faceted-searches-load-more?search=&page={i}")
            payload = json.loads(response)
            soup = BeautifulSoup(payload["html"], 'html.parser')
            anchors = soup.find_all("a", href=True)

            for a in anchors:
                href = a["href"]
                if href.startswith("https://www.allrecipes.com/recipe/") and not recipe_urls.get(href, False):
                    recipe_urls[href] = True
                    yield href

            if not payload["hasNext"]:
                break

            i += 1
