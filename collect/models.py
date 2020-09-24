from fractions import Fraction

from quantulum3 import parser


class Ingredient:

    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

    def __str__(self):
        amount = str(Fraction(self.amount))
        if str(self.unit) != "":
            return f"{amount} {self.unit} {self.name}"
        return f"{amount} {self.name}"


def ingredient_from_string(s):
    quantums = parser.parse(s)
    qu = quantums[0]

    s = s.replace(qu.to_spoken(), "")
    if str(qu.unit) != "":
        s = s.replace(f"{str(qu.unit)}s", "")
        s = s.replace(str(qu.unit), "")
    s = s.replace(str(Fraction(qu.value)), "")
    s = s.split(", ")[0]
    s = s.split(" - ")[0]
    s = s.lstrip(" ")
    return Ingredient(
        name=s,
        amount=qu.value,
        unit=qu.unit,
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
