import os

import requests


def _cache_path(resource):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../cache")
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)

    resource = resource.rstrip("/")
    if not resource.endswith("/index.html"):
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
            return content

    with open(path, "wb") as f:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(response.status_code)

        f.write(response.content)
        return response.content


def clean_str(s):
    s = str(s)
    s = s.replace("½", "1/2")
    s = s.replace("¼", "1/4")
    s = str(s).lstrip(" \\n\n\t").rstrip(" \\n\n\t").replace("  ", " ")
    return s
