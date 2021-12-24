import base64
import hashlib
import os
import pprint
import random
import uuid
from typing import Optional
from urllib.parse import urlparse

import sqlalchemy
from sqlalchemy import Column, String, JSON, ForeignKey, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import _get_recipe_metadata, get_cached

# from ingredients.parse import Parser

pwd = os.path.dirname(os.path.abspath(__file__))
engine = create_engine("sqlite:///" + os.path.join(pwd, "db.sqlite"))
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ingredient_parser = Parser()


class Recipe(Base):
    __tablename__ = 'recipes'
    pub_id = Column(String, primary_key=True)
    url = Column(String)
    title = Column(String)
    ingredients = Column(JSON)
    instructions = Column(JSON)
    tags = Column(JSON)
    images = Column(JSON)

    def __repr__(self):
        return f"<Recipe id='{self.pub_id}'>"

    @property
    def domain(self):
        return urlparse(self.url).hostname

    @property
    def filename(self):
        return f"{self.pub_id}.json"

    def save(self):
        session = Session()
        self.pub_id = Recipe.get_pub_id(self.url)
        qs = session.query(Recipe).filter(Recipe.pub_id == self.pub_id)
        if len(qs.all()) != 0:
            print(f"skipping, already got {self.pub_id}\t{self.url}")
            return
        _save_obj(self)

    #
    #     # save tags
    #     for tag in self.tags:
    #         obj = Tag(name=tag)
    #         _save_obj(RecipeTag(
    #             tag_name=tag,
    #             recipe_pub_id=self.pub_id
    #         ))
    #         obj.save()
    #
    #     # save ingredients
    #     ingredient_names = []
    #     for s in self.ingredients:
    #         data = ingredient_parser.parse(s)
    #         name = data["material"]
    #         if len(name) > 20 or len(name) <= 1:
    #             continue
    #         if name in ingredient_names:
    #             continue
    #         ingredient_names.append(name)
    #         obj = Ingredient(name=name)
    #         _save_obj(RecipeIngredient(
    #             ingredient_name=name,
    #             recipe_pub_id=self.pub_id
    #         ))
    #         obj.save()

    @classmethod
    def from_url(cls, url: str) -> Optional["Recipe"]:
        content = get_cached(url)
        if not content:
            return None

        recipe_metadata_json = _get_recipe_metadata(content)
        if not recipe_metadata_json:
            return None
        recipe = Recipe.parse(recipe_metadata_json)
        recipe.url = url
        return recipe

    @classmethod
    def get_pub_id(cls, url: str) -> str:
        hashid = hashlib.sha224(url.encode("ascii")).hexdigest()
        s = str(f"recipe_{hashid.replace('-', '')}")
        return s

    @classmethod
    def parse(cls, data: dict) -> "Recipe":
        url = data.get("mainEntityOfPage", "")
        if type(url) != str:
            if "url" in data:
                url = data["url"]
            else:
                url = url["@id"]
        pub_id = Recipe.get_pub_id(url)

        images = data["image"]
        if type(images) == str:
            images = [images]
        elif type(images) == list:
            if len(images) > 0 and type(images[0]) == list:
                images = [img["url"] for img in data["images"]]
        elif type(images) == dict:
            images = [data["image"]["url"]]

        instructions = data.get("recipeInstructions", [])
        if instructions:
            instructions = [d.get("text", "") for d in instructions]

        return Recipe(
            pub_id=pub_id,
            url=url,
            title=data["name"] if "name" in data else data["headline"],
            ingredients=data.get("recipeIngredient", []),
            instructions=instructions,
            tags=data.get("recipeCategory", []),
            images=images,
        )

    def get_tags(self):
        def clean(tag):
            tag = tag.replace("\"", "")
            tag = tag.replace(",", "")
            tag = tag.replace("(", "")
            tag = tag.replace(")", "")
            if len(tag) == 0:
                return None
            if tag[0] == "&":
                return None
            if tag[0] == "1":
                return None
            if tag[0] == "2":
                return None
            if tag[0] == "3":
                return None
            return tag

        self.tags = [clean(tag) for tag in self.tags if clean(tag) is not None]
        return self.tags

    def json(self):
        return {
            "pub_id": self.pub_id,
            "url": self.url,
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "tags": self.get_tags(),
            "images": self.images,
        }


class Tag(Base):
    __tablename__ = 'tags'
    name = Column(String, primary_key=True)
    count = Column(Integer)

    def recipe_pub_ids(self):
        session = Session()
        qs = session.query(RecipeTag).filter(RecipeTag.tag_name == self.name)
        recipe_pub_ids = [rt.recipe_pub_id for rt in qs.all()]
        return recipe_pub_ids

    def save(self):
        self.count = len(self.recipe_pub_ids())
        _save_obj(self)

    def __repr__(self):
        return f"<Tag name='{self.name}' count='{self.count}' >"


class RecipeTag(Base):
    __tablename__ = 'recipetags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String, ForeignKey('tags.name'))
    recipe_pub_id = Column(String, ForeignKey('recipes.pub_id'))

    def __repr__(self):
        return f"<RecipeTag recipe_pub_id='{self.recipe_pub_id}' name='{self.tag_name}'>"


class Ingredient(Base):
    __tablename__ = 'ingredients'
    name = Column(String, primary_key=True)
    count = Column(Integer)

    def recipe_pub_ids(self):
        session = Session()
        qs = session.query(RecipeIngredient).filter(RecipeIngredient.ingredient_name == self.name)
        recipe_pub_ids = [rt.recipe_pub_id for rt in qs.all()]
        return recipe_pub_ids

    def save(self):
        self.count = len(self.recipe_pub_ids())
        _save_obj(self)

    def __repr__(self):
        return f"<Ingredient ingredient='{self.name}'>"


class RecipeIngredient(Base):
    __tablename__ = 'recipeingredients'
    id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, ForeignKey('ingredients.name'))
    recipe_pub_id = Column(String, ForeignKey('recipes.pub_id'))

    def __repr__(self):
        return f"<RecipeIngredient recipe_pub_id='{self.recipe_pub_id}' ingredient='{self.ingredient_name}'>"


def _save_obj(obj):
    session = Session()
    session.add(obj)
    session.commit()


Base.metadata.create_all(engine)
