import hashlib
import os
from fractions import Fraction

import PIL
import boto3 as boto3
import botocore
import fractions
import requests
from PIL import Image
from quantulum3 import parser
import pattern.en

from api.utils import get_cached, get_cached_path, _cache_path


class Ingredient:

    def __init__(self, name, quantity, original, notes=""):
        self.name = name
        self.quantity = quantity
        self.orginal = original
        self.notes = notes

    def __str__(self):
        return f"{self.quantity.to_spoken()} {self.name}"

    def json(self):
        if self.quantity.value == 0.3333333333333333:
            self.quantity.value = 1/3
        f = fractions.Fraction(self.quantity.value)
        n = f.numerator
        d = f.denominator
        real = 0
        while n >= d:
            real += 1
            n -= d

        if n != 0:
            num = f"{n}/{d}"
            if real != 0:
                num = f"{real} {n}/{d}"
        if f.denominator == 1:
            num = f"{real}"
        num = num.replace("6004799503160661/18014398509481984", "1/3")

        spoken = f"{num}"
        if self.quantity.unit.name != "dimensionless":
            name = self.quantity.unit.name
            if self.quantity.value > 1:
                name = pattern.en.pluralize(name)
            spoken = f"{num} {name}"

        return {
            "name": self.name,
            "unit": self.quantity.unit.name,
            "value": self.quantity.value,
            "spoken": spoken,
            "original": self.orginal,
            "notes": self.notes,
        }


def ingredient_from_string(s):
    original = s
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
        original=original,
    )


def recipe_id(url):
    hashid = hashlib.sha224(url.encode("ascii")).hexdigest()
    return f"recipe_{hashid}"


def calc_filename(name, path, id, i):
    filename, file_extension = os.path.splitext(path)
    filepath = _cache_path(f"images/{name}/{id}.{i}.{name}.square{file_extension}")
    return filepath


def scale_to_square(id, path, i, desired_size=None, name="original"):
    im = Image.open(path)
    width, height = im.size
    size = width if width < height else height
    if desired_size is None:
        desired_size = size
    return scale(id, path, i, new_width=desired_size, new_height=desired_size, name=name)


def scale(id, path, i, new_width=512, new_height=512, name="original"):
    im = Image.open(path)
    width, height = im.size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    im = im.crop((left, top, right, bottom))
    im.thumbnail((new_width, new_height), Image.ANTIALIAS)

    filename, file_extension = os.path.splitext(path)
    filepath = _cache_path(f"images/{name}/{id}.{i}.{name}.square{file_extension.lower()}")
    im.save(filepath)
    return filepath


def save_to_s3(path, id, i):
    import boto3
    s3_client = boto3.client('s3')
    try:
        filepath = calc_filename("512", path, id, i)
        s3_client.head_object(
            Bucket="assets.recipes.oram.ca",
            Key=f"images/{os.path.basename(filepath)}",
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            filepath = scale_to_square(id, path, i, 512, "512")
            s3_client.upload_file(
                filepath,
                "assets.recipes.oram.ca",
                f"images/{os.path.basename(filepath)}",
                ExtraArgs={'ACL': 'public-read'}
            )
        else:
            raise
    if i == 0:
        filepath = scale(id, path, i, 1024, 128, "1024x128")
        s3_client.upload_file(
            filepath,
            "assets.recipes.oram.ca",
            f"images/{os.path.basename(filepath)}",
            ExtraArgs={'ACL': 'public-read'}
        )


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
            try:
                path, exists = get_cached_path(image_url)
                if path is None:
                    continue
                if not exists:
                    save_to_s3(path, self.id, i)
            except PIL.UnidentifiedImageError:
                continue
            except OSError:
                continue
            i += 1

    def json(self):

        def get_original_image(d):
            if type(d["originals"]) != list:
                return get_original_image(d["originals"])
            return d["originals"][0]

        return {
            "url": self.url,
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "tags": self.tags,
            "images": {
                "originals": get_original_image(self.images),
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

    @property
    def domain(self):
        parts = self.url.replace("https://", "").split("/")
        return parts[0]

    @classmethod
    def from_json(cls, data):
        recipe = Recipe(
            url = data.get("url"),
            title = data.get("title"),
            subtitle = data.get("subtitle"),
            ingredients = data.get("ingredients"),
            instructions = data.get("instructions"),
            category = data.get("category"),
            tags = data.get("tags"),
            images = data.get("images"),
            servings=1,
        )
        return recipe
