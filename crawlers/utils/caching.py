import enum
import json
import os
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def _cache_path(resource):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_path = os.path.join(dir_path, "../../cache")
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
    return path


def _get_recipe_metadata(content: str) -> Optional[dict]:
    soup = BeautifulSoup(content, 'html.parser')
    script_tags = soup.find_all("script", {"type": "application/ld+json"})
    for tag in script_tags:
        try:
            schema_datas = json.loads(tag.string.replace("\u2009", " "))
        except:
            continue
        if type(schema_datas) != list:
            schema_datas = [schema_datas]
        for schema_data in schema_datas:
            schema_type = schema_data.get("@type", "wrong")
            if schema_type == ["Recipe"]:
                schema_data["@type"] = "Recipe"
                return schema_data
            if schema_type == "Recipe":
                return schema_data

    return None


async def get_head_recipe(url):
    content = await get_cached(url)
    if not content:
        print("no content for url: ", url)
        return None
    return _get_recipe_metadata(content)


async def get_cached_request(url: str, cache_url: Optional[str] = None, attempts=0) -> Optional[bytes]:
    if cache_url is None:
        cache_url = url

    if attempts >= 3:
        return None

    path = _cache_path(cache_url)
    if os.path.exists(path):
        with open(path, "rb") as f:
            content = f.read()
            if len(content) == 0:
                remove_cached(url)
                return await get_cached_request(url)
            return content

    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as f:
        time.sleep(1)
        response = requests.get(url)
        content = response.content

        # if response.status_code >= 500 or response.status_code in [404, 403]:
        #     print(f"trying again {response.status_code} attempt {attempts}, url {url}, {response.content}")
        #     remove_cached(url)
        #     return get_cached(url, url, attempts+1)
        #
        # if response.status_code != 200:
        #     print(f"error for url: ({response.status_code}){url}")
        #     import pdb
        #     pdb.set_trace()
        #     raise Exception(response.status_code, response.content)

        f.write(content)
        return content


class GetMethod(enum.Enum):
    REQUESTS = 1
    PLAYWRIGHT = 2


async def _get_content(url: str, method:GetMethod.PLAYWRIGHT):
    if method == GetMethod.REQUESTS:
        try:
            content = requests.get(url).content.decode("utf-8")
            return content
        except Exception as e:
            print(e)
            return None

    elif method == GetMethod.PLAYWRIGHT:
        async def _get_content_async(url):
            p = await async_playwright().start()
            browser = await p.chromium.launch(headless=True)
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " \
                            "AppleWebKit/537.36 (KHTML, like Gecko) " \
                            "Chrome/90.0.4430.212 Safari/537.36"

            page = await browser.new_page(user_agent=user_agent)
            retries = 0
            while True:
                if retries >= 3:
                    print("failed to load page")
                    return None
                try:
                    referrer = "https://"+url.split("/")[2]
                    response = await page.goto(url, referer=referrer, timeout=10000)
                    if response.status == 200:
                        break
                    retries += 1
                    print("retrying status code", response.status)
                except:
                    print("retrying")
                    retries += 1
                    time.sleep(1)
            content = await page.content()
            await page.close()
            return content
        return await _get_content_async(url)
    else:
        raise Exception(f"Unknown method {method}")


async def get_cached(url: str, cache_url: Optional[str] = None, attempts=0) -> Optional[str]:
    if cache_url is None:
        cache_url = url

    if attempts >= 3:
        return None

    path = _cache_path(cache_url)
    if len(path) > 255:
        return None
    if os.path.exists(path):
        with open(path, "rb") as f:
            content = f.read()
            if "403 Forbidden" in content.decode("utf-8"):
                remove_cached(cache_url)
                time.sleep(1)
                return await get_cached(url, attempts=attempts + 1)
            if len(content) == 0:
                remove_cached(cache_url)
                return await get_cached(url, attempts=attempts+1)
            return content

    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "w") as f:
        time.sleep(1)
        content = await _get_content(url, method=GetMethod.REQUESTS)
        if content is None:
            return None
        f.write(content)
        return content


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
        if response.status_code == 404:
            return None, False
        if response.status_code != 200:
            raise Exception(response.status_code)

        f.write(response.content)
        return path, False


def clean_str(s):
    s = str(s)
    s = s.replace("½", "1/2")
    s = s.replace("⅓", "1/3")
    s = s.replace("¼", "1/4")
    s = s.replace(" 1/2", ".5")
    s = s.replace("1/2", "0.5")
    s = s.replace("1/2", "0.5")
    s = str(s).lstrip(" \\n\n\t").rstrip(" \\n\n\t").replace("  ", " ")
    return s
