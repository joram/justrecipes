import stem
from models import Recipe
from nltk.stem import PorterStemmer

from api.utils import recipe_exists, remove_cached

ps = PorterStemmer()


class BaseCrawler:

    domain = "base"

    def next_recipe(self, skip_existing=False):
        for url in self.get_recipe_urls():
            if skip_existing and recipe_exists(Recipe(url=url, servings=1, title="", subtitle="")):
                yield None
                continue

            # try:
            try:
                r = self.get_recipe(url)
            except:
                print(f"failed on: {url}")
                raise
            yield r
            # except Exception as e:
            #     print("error with:", url)
            #     # remove_cached(url)

    @property
    def remaining(self):
        raise NotImplemented

    def get_recipe_urls(self):
        raise NotImplemented

    def get_recipe(self, url):
        raise NotImplemented
