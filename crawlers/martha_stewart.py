import json
import re

import requests
from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler
from utils import get_cached


class MarthaStewart(BaseCrawler):

    domain = "marthastewart.com"
    recipe_url_regex = re.compile('https://www.marthastewart.com/\d+/.*')

    def get_recipe_urls(self):
        recipe_urls = {}
        i = 1
        while True:
            response = get_cached(f"https://www.marthastewart.com/element-api/content-proxy/site-search?page={i}")
            payload = json.loads(response)
            soup = BeautifulSoup(payload["html"], 'html.parser')
            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if self.recipe_url_regex.match(href) and not recipe_urls.get(href, False):
                    recipe_urls[href] = True
                    yield href
            if not payload["hasNext"]:
                return
            i += 1
