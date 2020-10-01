import json
import os
import time

import requests


def _cache_path(resource):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../cache")
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

    resource = resource.rstrip("/")

    has_valid_ending = False
    valid_endings = ["/index.html", ".jpg", ".jpeg", ".JPG", ".gif", ".png"]
    for valid_ending in valid_endings:
        if resource.endswith(valid_ending):
            has_valid_ending = True
            break
    if not has_valid_ending:
        resource = f"{resource}/index.html"

    path = os.path.join(
        os.path.abspath(cache_path),
        resource.lstrip("https://"),
    )

    resource_dir = os.path.dirname(path)
    if not os.path.exists(resource_dir):
        os.makedirs(resource_dir)
    return path


def get_cached(url):
    path = _cache_path(url)
    if os.path.exists(path):
        with open(path, "rb") as f:
            content = f.read()
            if len(content) == 0:
                remove_cached(url)
                return get_cached(url)
            return content

    with open(path, "wb") as f:
        time.sleep(1)
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            raise Exception(response.status_code)

        f.write(response.content)
        return response.content


def remove_cached(url):
    path = _cache_path(url)
    if os.path.exists(path):
        os.remove(path)


def get_cached_path(url):
    path = _cache_path(url)
    if os.path.exists(path):
        return path, True

    with open(path, "wb") as f:
        time.sleep(1)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response.status_code)

        f.write(response.content)
        return path, False


def recipe_exists(recipe):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../recipes/", recipe.filename)
    return os.path.exists(cache_path)


def store_recipe(recipe, overwrite=False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../recipes/", recipe.filename)
    if os.path.exists(cache_path) and not overwrite:
        return

    with open(cache_path, "w") as f:
        s = json.dumps(recipe.json(), indent=4, sort_keys=True)
        f.write(s)


def store_recipes(recipes):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../recipes.json")
    with open(cache_path, "w") as f:
        s = json.dumps(recipes, indent=4, sort_keys=True)
        f.write(s)


def clean_str(s):
    s = str(s)
    s = s.replace("½", "1/2")
    s = s.replace("⅓", "1/3")
    s = s.replace("¼", "1/4")
    s = s.replace("1/2", "0.5")
    s = str(s).lstrip(" \\n\n\t").rstrip(" \\n\n\t").replace("  ", " ")
    return s


def store_tags(tags):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../tags.json")
    with open(cache_path, "w") as f:
        s = json.dumps(tags, indent=4, sort_keys=True)
        f.write(s)


def load_tags():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../tags.json")
    with open(cache_path) as f:
        content = f.read()
        return json.loads(content)


def load_recipes():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../recipes.json")
    if not os.path.exists(cache_path):
        return {}
    with open(cache_path) as f:
        content = f.read()
        return json.loads(content)
