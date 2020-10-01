import urllib.parse

from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler
from models import ingredient_from_string, Recipe
from utils import get_cached, clean_str, recipe_exists


class AllRecipes(BaseCrawler):

    domain = "allrecipes"
    to_visit_list_urls = ["https://www.allrecipes.com/recipes/"]

    @property
    def remaining(self):
        return len(self.to_visit_list_urls)

    def get_recipe(self, url):
        original_url = url
        content = get_cached(url)
        content = content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        title = soup.find("h1", {"class": "headline"})
        if title is None:
            title = soup.find("h1", {"id": "recipe-main-content"})
        if title is None:
            return None
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

        images = []
        div = soup.find("div", {"class": "hero-photo__wrap"})
        if div is not None:
            a = div.find("a")
            imgs_content = get_cached(a.attrs["href"])
            imgs_content = imgs_content.decode('utf-8')
            for line in imgs_content.split("\n"):
                if "urls:" in line:
                    url = line.split("'")[1]
                    images.append(url)
        divs = soup.findAll("div", {"class": "lazy-image"})
        for div in divs:
            btn = div.find("button")
            if btn is not None:
                url = btn.attrs["data-image"]
                url = url.split("url=")[1]
                url = urllib.parse.unquote(url)
                images.append(url)
        recipe_div = soup.find("div", {"class": "recipe-content-container"})
        if recipe_div is not None:
            img = recipe_div.find("img")
            if img is not None:
                url = img.attrs["src"]
                try:
                    url = url.split("url=")[1]
                    url = url.split("?")[0]
                    url = urllib.parse.unquote(url)
                except:
                    pass
                images.append(url)
        images = [img for img in images if "media-allrecipes.com" in img]

        spans = soup.findAll("span", {"class": "breadcrumbs__title"})
        category = [span.text.strip("\n ") for span in spans]
        category = category[2:]
        return Recipe(
            url=original_url,
            title=title,
            subtitle="",
            ingredients=ingredients,
            instructions=steps,
            servings=servings,
            tags=self.clean_tags(category),
            images=images,
        )

    def get_recipe_urls(self):
        visited_list_urls = {}
        recipe_urls = {}
        i = 0
        while len(self.to_visit_list_urls) > 0:
            list_url = self.to_visit_list_urls[0]
            self.to_visit_list_urls = self.to_visit_list_urls[1:]

            if i % 100 == 0:
                print(f"got {len(self.to_visit_list_urls)} urls to visit")
            i += 1

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
                if "/recipe/" in href and not recipe_urls.get(href, False):
                    recipe_urls[href] = True
                    yield href
                if "/recipes/" in href and not visited_list_urls.get(href, False):
                    visited_list_urls[href] = True
                    self.to_visit_list_urls.append(href)
