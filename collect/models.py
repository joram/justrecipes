from fractions import Fraction


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
