import requests

from base import BaseCrawler


class BBCGoodFood(BaseCrawler):
    async def get_recipe_urls(self):
        page = 1
        while True:
            response = requests.get(f"https://www.bbcgoodfood.com/api/search-frontend/search?q=&page={page}")
            if response.status_code != 200:
                break
            data = response.json()
            results = data.get("searchResults", {}).get("items", [])
            for item in results:
                yield f"https://www.bbcgoodfood.com{item['url']}"
            page += 1
