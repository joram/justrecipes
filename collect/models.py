from fractions import Fraction

from quantulum3 import parser


class Ingredient:

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.quantity.to_spoken()} {self.name}"


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

    def __init__(self, title, subtitle, servings, ingredients=[], instructions=[]):
        """
        :param title: string
        :param subtitle: string
        :param servings: int
        :param ingredients: list<Ingredient>
        :param instructions: list<str>
        """
        self.title = title
        self.subtitle = subtitle
        self.ingredients = ingredients
        self.instructions = instructions

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
