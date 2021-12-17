#!/usr/bin/env python

from bs4 import BeautifulSoup

from api.utils import get_cached
from collect.crawlers.base import BaseCrawler


class AsEasyAsApplePie(BaseCrawler):
    domain = "applepie"

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
