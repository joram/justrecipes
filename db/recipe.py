import hashlib
from urllib.parse import urlparse

from parse_ingredients import parse_ingredient
from sqlalchemy import Column, String, JSON

from db.session import Base, Session


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

    def save(self, override=False):
        session = Session()
        self.pub_id = Recipe.get_pub_id(self.url)
        qs = session.query(Recipe).filter(Recipe.pub_id == self.pub_id)
        if len(qs.all()) != 0:
            if override:
                qs.delete()
            else:
                print(f"skipping, already got {self.pub_id}\t{self.url}")
                return
        _save_obj(self)

        # # save tags
        # for tag in self.tags:
        #     obj = Tag(name=tag)
        #     _save_obj(RecipeTag(
        #         tag_name=tag,
        #         recipe_pub_id=self.pub_id
        #     ))
        #     obj.save()
        #
        # # save ingredients
        # ingredient_names = []
        # for s in self.ingredients:
        #     data = ingredient_parser.parse(s)
        #     name = data["material"]
        #     if len(name) > 20 or len(name) <= 1:
        #         continue
        #     if name in ingredient_names:
        #         continue
        #     ingredient_names.append(name)
        #     obj = Ingredient(name=name)
        #     _save_obj(RecipeIngredient(
        #         ingredient_name=name,
        #         recipe_pub_id=self.pub_id
        #     ))
        #     obj.save()

    @classmethod
    def get_pub_id(cls, url: str) -> str:
        hashid = hashlib.sha224(url.encode("ascii")).hexdigest()
        s = str(f"recipe_{hashid.replace('-', '')}")
        return s

    @classmethod
    def parse(cls, data: dict, url: str) -> "Recipe":
        pub_id = Recipe.get_pub_id(url)

        title = data["name"] if "name" in data else data["headline"]

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
            title=title,
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

    @property
    def detailed_ingredients(self):
        detailed_ingredients = []
        for ingredient in self.ingredients:
            ingredient = ingredient.replace("-", " ")
            try:
                result = parse_ingredient(ingredient)
            except:
                continue
            detailed_ingredients.append({
                "name": result.name,
                "quantity": result.quantity,
                "unit": result.unit,
                "comment": result.comment,
                "original_string": result.original_string
            })
        return detailed_ingredients

    def json(self):
        return {
            "pub_id": self.pub_id,
            "url": self.url,
            "title": self.title,
            "ingredients": self.ingredients,
            "ingredient_details": self.detailed_ingredients,
            "instructions": self.instructions,
            "tags": self.get_tags(),
            "images": self.images,
        }


def _save_obj(obj: Base):
    session = Session()
    session.add(obj)
    session.commit()


