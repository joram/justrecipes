from utils import get_cached, clean_str, recipe_exists
from models import Recipe


class BaseCrawler:

    def next_recipe(self, skip_existing=False):
        for url in self.get_recipe_urls():
            if skip_existing and recipe_exists(Recipe(url=url, servings=1, title="", subtitle="")):
                yield None
                continue

            try:
                r = self.get_recipe(url)
            except Exception as e:
                print("error with:", url)
                print(e)
                continue
            yield r

    def get_recipe_urls(self):
        raise NotImplemented

    def get_recipe(self, url):
        raise NotImplemented
