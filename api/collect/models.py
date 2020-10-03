import hashlib
import os
from fractions import Fraction

import boto3 as boto3
import requests
from PIL import Image
from quantulum3 import parser

from utils import get_cached, get_cached_path, _cache_path


class Ingredient:

    def __init__(self, name, quantity, notes=""):
        self.name = name
        self.quantity = quantity
        self.notes = notes

    def __str__(self):
        return f"{self.quantity.to_spoken()} {self.name}"

    def json(self):
        return {
            "name": self.name,
            "unit": self.quantity.unit.name,
            "value": self.quantity.value,
            "spoken": self.quantity.to_spoken(),
            "notes": self.notes,
        }


def ingredient_from_string(s):
    s = s.replace(" ", " ")

    quantums = parser.parse(s)
    try:
        qu = quantums[0]
    except:
       return None

    s = s.replace(qu.to_spoken(), "")
    if str(qu.unit) != "":
        s = s.replace(f"{str(qu.unit)}s", "")
        s = s.replace(str(qu.unit), "")
    s = s.replace(str(Fraction(qu.value)), "")
    s = s.split(", ")[0]
    s = s.split(" - ")[0]
    for i in range(0, 9):
        s = s.replace(str(i), "")
    s = s.replace("/", "")
    s = s.lstrip(" ")

    return Ingredient(
        name=s,
        quantity=qu,
    )


def recipe_id(url):
    hashid = hashlib.sha224(url.encode("ascii")).hexdigest()
    return f"recipe_{hashid}"


class Recipe:

    def __init__(self, url, title, subtitle, servings, ingredients=[], instructions=[], category=[], tags=[], images=[]):
        """
        :param url:string the source url
        :type url: str
        :param title:
        :type title: str
        :param subtitle:
        :type subtitle: string
        :param servings:
        :type servings: int
        :param ingredients:
        :type ingredients: list Ingredient
        :param instructions:
        :type instructions: list str
        :param category:
        :type category: list str
        :param tags:
        :type tags: list str
        :param images:
        :type images: list str
        """
        self.url = url
        self.title = title
        self.subtitle = subtitle
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category
        self.tags = [tag.lower() for tag in tags]
        self.images = images

    def __str__(self):
        return self.title

    def store_images(self):
        if len(self.images) == 0:
            return
        i = 0
        for image_url in self.images:

            def scale_to_square(path, i, desired_size=None, name="original"):
                im = Image.open(path)
                width, height = im.size
                size = width if width < height else height
                if desired_size is None:
                    desired_size = size
                left = (width - size) / 2
                top = (height - size) / 2
                right = (width + size) / 2
                bottom = (height + size) / 2
                im = im.crop((left, top, right, bottom))
                im.thumbnail((desired_size, desired_size), Image.ANTIALIAS)

                filename, file_extension = os.path.splitext(path)
                filepath = _cache_path(f"images/{name}/{self.id}.{i}.{name}.square{file_extension}")
                im.save(filepath)
                return filepath

            def save_to_s3(filepath):
                import boto3
                s3_client = boto3.client('s3')
                response = s3_client.upload_file(
                    filepath,
                    "assets.recipes.oram.ca",
                    f"images/{os.path.basename(filepath)}",
                    ExtraArgs={'ACL': 'public-read'}
                )


            try:
                path, exists = get_cached_path(image_url)
                # if not exists:
                filepath = scale_to_square(path, i, 512, "512")
                save_to_s3(filepath)
            except:
                print(image_url)
            i += 1

    def json(self):
        try:
            ingredients_json = [i.json() for i in self.ingredients]
        except:
            ingredients_json = {}
            for section in self.ingredients:
                ingredients_json[section] = [i.json() for i in self.ingredients[section]]

        return {
            "url": self.url,
            "title": self.title,
            "subtitle": self.subtitle,
            "ingredients": ingredients_json,
            "instructions": self.instructions,
            "category": self.category,
            "tags": self.tags,
            "images": {
                "originals": self.images,
                "x512": [f"https://s3-us-west-2.amazonaws.com/assets.recipes.oram.ca/images/{self.id}.{i}.512.square.jpg" for i in range(0, len(self.images))],
            },
            "id": self.id,
        }

    @property
    def id(self):
        return recipe_id(self.url)

    @property
    def filename(self):
        return f"{self.id}.json"
