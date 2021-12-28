from db.session import Base, engine, Session

from db.recipe import Recipe
from db.ingredient import Ingredient, RecipeIngredient
from db.tag import Tag, RecipeTag

Base.metadata.create_all(engine)
