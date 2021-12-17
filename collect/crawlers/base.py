import stem
from models import Recipe
from nltk.stem import PorterStemmer
from recipe_scrapers import scrape_me

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
        scraper = scrape_me(url, wild_mode=True)
        # scraper.title()
        # scraper.total_time()
        # scraper.yields()
        # scraper.ingredients()
        # scraper.instructions()
        # scraper.image()
        # scraper.host()
        # scraper.links()
        # scraper.nutrients()  # if available
        try:
            return Recipe(
                url=url,
                title=scraper.title(),
                subtitle="",
                ingredients=scraper.ingredients(),
                instructions=scraper.instructions(),
                servings=scraper.yields(),
                tags=[],
                images=[scraper.image()],
            )
        except Exception as e:
            print(e)
