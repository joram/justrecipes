import os
from urllib.parse import urlparse

import sqlalchemy
from sqlalchemy import Column, String, JSON, ForeignKey, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pwd = os.path.dirname(os.path.abspath(__file__))
engine = create_engine("sqlite:///" + os.path.join(pwd, "db.sqlite"))
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Recipe(Base):
    __tablename__ = 'recipes'
    pub_id = Column(String, primary_key=True)
    url = Column(String)
    title = Column(String)
    ingredients = Column(JSON)
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
            tags=recipe.tags,
            images=recipe.images,
        )

    def json(self):
        return {
            "pub_id": self.pub_id,
            "url": self.url,
            "title": self.title,
            "ingredients": self.ingredients,
            "tags": self.tags,
            "images": self.images,
        }

    def save(self):
        _save_obj(self)
        for tag in self.tags:
            _save_obj(Tag(name=tag))
            _save_obj(RecipeTag(
                tag_name=tag,
                recipe_pub_id=self.pub_id
            ))


class Tag(Base):
    __tablename__ = 'tags'
    name = Column(String, primary_key=True)
    count = Column(Integer)

    def __repr__(self):
        return f"<Tag name='{self.name}'>"


class RecipeTag(Base):
    __tablename__ = 'recipetags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String, ForeignKey('tags.name'))
    recipe_pub_id = Column(String, ForeignKey('recipes.pub_id'))

    def __repr__(self):
        return f"<RecipeTag recipe_pub_id='{self.recipe_pub_id}' name='{self.tag_name}'>"


def _save_obj(obj):
    session = Session()
    session.add(obj)
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass

Base.metadata.create_all(engine)
