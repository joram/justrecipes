from bs4 import BeautifulSoup

from base import BaseCrawler
from utils.caching import get_cached


class NYTimes(BaseCrawler):

    domain = "cooking.nytimes.com"
    to_visit_list_urls = ["https://cooking.nytimes.com/search?q=&page=1"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

    async def get_recipe_urls(self):
        recipe_urls = {}
        i = 1
        while i < 24:
            list_url = f"https://cooking.nytimes.com/search?q=&page={i}"
            content = await get_cached(list_url)
            if not content:
                continue
            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if href.startswith("/") and "recipes" in href:
                    href = f"https://cooking.nytimes.com{href}"
                    if not recipe_urls.get(href, False):
                        recipe_urls[href] = True
                        yield href
                if href.startswith("/") and "cooking" in href:
                    href = f"https://cooking.nytimes.com{href}"
                    content = await get_cached(href)
                    if not content:
                        continue
                    soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
                    recipe_anchors = soup.find_all("a", href=True)
                    for a in recipe_anchors:
                        href = a["href"]
                        if href.startswith("/") and "recipes" in href:
                            href = f"https://cooking.nytimes.com{href}"
                            if not recipe_urls.get(href, False):
                                recipe_urls[href] = True
                                yield href

            i += 1
