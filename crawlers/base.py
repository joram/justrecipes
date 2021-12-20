from nltk.stem import PorterStemmer

from utils import recipe_exists
from db.recipe import Recipe

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

    @property
    def remaining(self):
        raise NotImplemented

    def get_recipe_urls(self):
        raise NotImplemented

    def get_recipe(self, url):
        return Recipe.from_url(url)
