from typing import Tuple

from nltk.stem import PorterStemmer

from utils import get_head_recipe

ps = PorterStemmer()


class BaseCrawler:

    domain = "base"

    def next_recipe(self) -> Tuple[dict, str]:
        visited_urls = []
        for url in self.get_recipe_urls():
            if url in visited_urls:
                continue
            visited_urls.append(url)
            yield get_head_recipe(url), url

    def get_recipe_urls(self):
        raise NotImplemented

