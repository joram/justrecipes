from sqlalchemy import Column, Integer, String, ForeignKey

from db.recipe import _save_obj
from db.session import Base, Session


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




