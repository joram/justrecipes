from sqlalchemy import Column, String, ForeignKey, Integer

from db.recipe import _save_obj
from db.session import Base, Session


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
        _save_obj(self)

    def __repr__(self):
        return f"<Ingredient ingredient='{self.name}'>"


class RecipeIngredient(Base):
    __tablename__ = 'recipeingredients'
    id = Column(Integer, primary_key=True)
    ingredient_name = Column(String, ForeignKey('ingredients.name'))
    recipe_pub_id = Column(String, ForeignKey('recipes.pub_id'))

    def save(self):
        _save_obj(self)

    def __repr__(self):
        return f"<RecipeIngredient recipe_pub_id='{self.recipe_pub_id}' ingredient='{self.ingredient_name}'>"
