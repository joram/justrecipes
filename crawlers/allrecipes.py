from bs4 import BeautifulSoup

from utils import get_cached
from crawlers.base import BaseCrawler


class AllRecipes(BaseCrawler):

    domain = "allrecipes"
    to_visit_list_urls = ["https://www.allrecipes.com/recipes/"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

    def get_recipe_urls(self):
        visited_list_urls = {}
        recipe_urls = {}
        i = 0
        while len(self.to_visit_list_urls) > 0:
            list_url = self.to_visit_list_urls[0]
            self.to_visit_list_urls = self.to_visit_list_urls[1:]

            try:
                content = get_cached(list_url)
            except:
                content = get_cached(list_url.split("?")[0])

            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if not href.startswith("http"):
                    continue
                if "/recipe/" in href and not recipe_urls.get(href, False):
                    recipe_urls[href] = True
                    yield href
                if "/recipes/" in href and not visited_list_urls.get(href, False):
                    visited_list_urls[href] = True
                    self.to_visit_list_urls.append(href)
            i += 1
