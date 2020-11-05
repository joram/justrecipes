import os
from urllib.parse import urlparse

import sqlalchemy
from sqlalchemy import Column, String, JSON, ForeignKey, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ingredients.parse import Parser

pwd = os.path.dirname(os.path.abspath(__file__))
engine = create_engine("sqlite:///" + os.path.join(pwd, "db.sqlite"))
Base = declarative_base()
Session = sessionmaker(bind=engine)
ingredient_parser = Parser()


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

    @classmethod
    def from_json(cls, recipe):
        return Recipe(
            pub_id=recipe.id,
            url=recipe.url,
            title=recipe.title,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            tags=recipe.tags,
            images=recipe.images,
        )

    def json(self):
        return {
            "pub_id": self.pub_id,
            "url": self.url,
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "tags": self.tags,
            "images": self.images,
        }

    def save(self):
        # save self
        _save_obj(self)

        # save tags
        for tag in self.tags:
            obj = Tag(name=tag)
            _save_obj(RecipeTag(
                tag_name=tag,
                recipe_pub_id=self.pub_id
            ))
            obj.save()

        # save ingredients
        ingredient_names = []
        for section in self.ingredients:
            for s in self.ingredients[section]:
                data = ingredient_parser.parse(s)
                name = data["material"]
                if len(name) > 20 or len(name) <= 1:
                    continue
                if name in ingredient_names:
                    continue
                ingredient_names.append(name)
                obj = Ingredient(name=name)
                _save_obj(RecipeIngredient(
                    ingredient_name=name,
                    recipe_pub_id=self.pub_id
                ))
                _save_obj(obj)

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
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass

Base.metadata.create_all(engine)
