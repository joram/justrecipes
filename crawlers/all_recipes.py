from bs4 import BeautifulSoup

from base import BaseCrawler
from utils.queue_manager import get_queue_manager
from utils.caching import get_cached

class AllRecipes(BaseCrawler):

    domain = "allrecipes.com"

    async def get_links(self, url):
        content = await get_cached(url)
        soup = BeautifulSoup(content, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                href = f"https://www.allrecipes.com{href}"
            links.append(href)
        return links

    async def is_recipe_page(self, url) -> bool:
        try:
            content = await get_cached(url)
        except:
            return False
        if not content:
            return False
        soup = BeautifulSoup(content, "html.parser")
        head_recipe = soup.find_all("script", {"id": "allrecipes-schema_1-0"})
        return len(head_recipe) > 0

    async def get_recipe_urls(self):
        get_queue_manager().add_urls_to_visit(["https://www.allrecipes.com/recipe/74422/classic-cherries-jubilee/", "https://www.allrecipes.com/"])
        while True:
            urls = get_queue_manager().get_urls_to_visit(1)
            if len(urls) == 0:
                return

            url = urls[0]
            get_queue_manager().mark_url_visited(url)

            if not url.startswith("https://www.allrecipes.com/"):
                continue
            is_recipe = await self.is_recipe_page(url)
            if is_recipe:
                yield url

            links = await self.get_links(url)
            get_queue_manager().add_urls_to_visit(links)
