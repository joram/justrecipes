from typing import Tuple, AsyncGenerator

from nltk.stem import PorterStemmer

from utils.caching import get_head_recipe

ps = PorterStemmer()


class BaseCrawler:

    domain = "base"

    async def next_recipe(self) -> Tuple[dict, str]:
        visited_urls = []
        generator = self.get_recipe_urls()
        while True:
            url = await generator.__anext__()
            if url in visited_urls:
                continue
            visited_urls.append(url)
            recipe = await get_head_recipe(url)
            yield recipe, url

    async def get_recipe_urls(self) -> AsyncGenerator[str, None]:
        raise NotImplemented

