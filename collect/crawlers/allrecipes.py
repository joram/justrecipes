from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler
from models import ingredient_from_string, Recipe
from utils import get_cached, clean_str, recipe_exists


class AllRecipes(BaseCrawler):

    def next_recipe(self, skip_existing=False):
        for url in self.get_allrecipes_urls():
            if skip_existing and recipe_exists(Recipe(url=url, servings=1, title="", subtitle="")):
                yield None
                continue

            try:
                r = self.get_allrecipes_recipe(url)
                yield r
            except Exception:
                print(url)

    def get_allrecipes_recipe(self, url):
        content = get_cached(url)
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

        title = soup.find("h1", {"class": "headline"})
        if title is None:
            title = soup.find("h1", {"id": "recipe-main-content"})
        title = str(title.text)

        ingredients = []
        lis = soup.findAll("li", {"class": "ingredients-item"})
        if len(lis) == 0:
            lis = soup.findAll("span", {"itemprop": "recipeIngredient"})
        for li in lis:
            s = clean_str(li.text)
            i = ingredient_from_string(s)
            if i is not None:
                ingredients.append(i)

        steps = []
        divs = soup.findAll("div", {"class": "paragraph"})
        if len(divs) == 0:
            divs = soup.findAll("span", {"class": "recipe-directions__list--item"})
        for div in divs:
            step = clean_str(div.text)
            steps.append(step)

        servings = None
        divs = soup.findAll("div", {"class": "recipe-meta-item"})
        for div in divs:
            key = clean_str(div.find("div", {"class": "recipe-meta-item-header"}))
            val = clean_str(div.find("div", {"class": "recipe-meta-item-body"}))
            if key.lower() == "yield:":
                servings = clean_str(val.text)
                break

        return Recipe(
            url=url,
            title=title,
            subtitle="",
            ingredients=ingredients,
            instructions=steps,
            servings=servings,
        )

    def get_allrecipes_urls(self):
        list_urls = ["https://www.allrecipes.com/recipes/"]
        recipe_urls = []
        for list_url in list_urls:
            try:
                content = get_cached(list_url)
            except:
                content = get_cached(list_url.split("?")[0])

            soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')

            anchors = soup.find_all("a", href=True)
            for a in anchors:
                href = a["href"]
                if not href.startswith("http"):
                    continue
                if "/recipe/" in href and href not in recipe_urls:
                    recipe_urls.append(href)
                    yield href
                if "/recipes/" in href and href not in list_urls:
                    list_urls.append(href)
