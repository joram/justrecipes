import hashlib
from fractions import Fraction

from quantulum3 import parser


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


class Recipe:

    def __init__(self, url, title, subtitle, servings, ingredients=[], instructions=[], category=[]):
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
        """
        self.url = url
        self.title = title
        self.subtitle = subtitle
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category

    def __str__(self):
        ingredient_list = [f"  {i}" for i in self.ingredients]
        ingredients = '\n'.join(ingredient_list)
        steps = "\n".join([f" {s}" for s in self.instructions])
        return f"<Recipe name='{self.title}'>\n" \
               f" <Ingredients>\n" \
               f"{ingredients}\n" \
               f" </Ingredients>\n" \
               f" <Instructions>\n" \
               f"{steps}\n" \
               f" </Instructions>\n" \
               f"</Recipe>"

    def json(self):
        return {
            "url": self.url,
            "title": self.title,
            "subtitle": self.subtitle,
            "ingredients": [i.json() for i in self.ingredients],
            "instructions": self.instructions,
            "category": self.category,
        }

    @property
    def filename(self):
        hash = hashlib.sha224(self.url.encode("ascii")).hexdigest()
        filename = f"recipe_{hash}.json"
        return filename