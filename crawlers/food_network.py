import logging

from bs4 import BeautifulSoup

from utils import get_cached
from crawlers.base import BaseCrawler

logger = logging.Logger(__name__)


class FoodNetwork(BaseCrawler):

    domain = "foodnetwork.com"
    to_visit_list_urls = ["https://www.allrecipes.com/recipes/"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

    def get_recipe_urls(self):
        i = 0
        while True:
            i += 1
            list_url = f"https://www.foodnetwork.com/search/-/p/{i}"
            content = get_cached(list_url)
            if content is None:
                logger.info(f"completed {self.domain}")
                return
            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if href.startswith("//"):
                    href = f"https:{href}"
                if "recipes/photos" in href:
                    content2 = get_cached(href)
                    soup2 = BeautifulSoup(content2.decode('utf-8'), 'html.parser')
                    anchors2 = soup2.find_all("a", href=True)
                    for a in anchors2:
                        href = a["href"]
                        if href.startswith("//"):
                            href = f"https:{href}"
                        if "recipes/food-network-kitchen" in href:
                            yield href
