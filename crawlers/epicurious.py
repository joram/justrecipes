from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler
from utils import get_cached


class Epicurious(BaseCrawler):

    domain = "epicurious"
    to_visit_list_urls = [
        "https://www.epicurious.com/recipes-menus/best-brunch-recipes-relaxing-weekend-breakfast-gallery"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

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