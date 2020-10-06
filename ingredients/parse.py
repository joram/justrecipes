import csv
import os
import pprint
import time
from fractions import Fraction
import pattern.en

from quantulum3 import parser as q3_parser

# Data sourced from:
# https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/nutrient-data/canadian-nutrient-file-2015-download-files.html
from api.utils import load_recipes


def load_csv(path, data_key):
    data = {}
    with open(path, encoding='iso-8859-1') as f:
        rows = csv.reader(f)
        headers = rows.__next__()
        print(headers)
        for row in rows:
            row_dict = {}
            for i in range(0, len(headers)):
                key = headers[i]
                val = row[i]
                row_dict[key] = val
            key = row_dict[data_key]
            if key == "":
                continue
            if key not in data:
                data[key] = []
            data[key].append(row_dict)
    print(len(data))
    return data


class Parser:

    # def __init__(self):
    #     curr_dir = os.path.dirname(os.path.abspath(__file__))
    #     self.conversion_factor_by_food_id = load_csv(os.path.join(curr_dir, "./data/CONVERSION FACTOR.csv"), "FoodID")
    #     self.food_group_by_id = load_csv(os.path.join(curr_dir, "./data/FOOD GROUP.csv"), "FoodGroupID")
    #     self.food_source_by_id = load_csv(os.path.join(curr_dir, "./data/FOOD SOURCE.csv"), "FoodSourceID")
    #     self.food_by_id = load_csv(os.path.join(curr_dir, "./data/FOOD NAME.csv"), "FoodID")
    #     self.food_by_description = load_csv(os.path.join(curr_dir, "./data/FOOD NAME.csv"), "FoodDescription")
    #
    #     self.nutrient_name_by_id = load_csv(os.path.join(curr_dir, "./data/NUTRIENT NAME.csv"), "NutrientID")
    #     self.nutrient_amount_by_food_id = load_csv(os.path.join(curr_dir, "./data/NUTRIENT AMOUNT.csv"), "FoodID")
    #
    #     self.yield_amount_by_food_id = load_csv(os.path.join(curr_dir, "./data/YIELD AMOUNT.csv"), "FoodID")
    #     self.yield_name_by_yield_id = load_csv(os.path.join(curr_dir, "./data/YIELD NAME.csv"), "YieldID")

    def _clean_string(self, s):
        s = s.replace(" ", " ")
        s = s.replace(" (blank)s ", " ")
        s = s.lstrip(" ").rstrip(" ")
        s = s.replace("½", "1/2")
        s = s.replace("⅓", "1/3")
        s = s.replace("¼", "1/4")
        s = s.replace("¾", "3/4")
        s = s.replace(" 1/2", ".5")
        s = s.replace("1/2", "0.5")
        s = s.replace("1/2", "0.5")
        return s

    def _get_comment(self, s):
        parts = s.split(",")
        comment = ""
        if len(parts) > 1:
            comment = self._clean_string(",".join(parts[1:]))
            s = parts[0]
        if "(" in s and ")" in s:
            comment2 = self._clean_string(s[s.find("(")+1:s.rfind(")")])
            remainder = s.replace(f"({comment2})", "")
            comment = comment2 if comment == "" else f"{comment}, {comment2}"
            return comment, remainder
        return comment, s

    def _get_quantities(self, s):
        quantums = q3_parser.parse(s)
        if len(quantums) == 0:
            return [(1, "")], s

        remainder = s
        quantities = []
        for quantum in quantums:
            quantity = quantum.value
            unit = quantum.unit.name
            if unit == "dimensionless":
                unit = ""

            unit_pluralized = ""
            if unit != "":
                unit_pluralized = unit if quantity <= 1 else pattern.en.pluralize(unit)

            f = Fraction(quantity)
            print(str(f))
            remainder = remainder.replace(str(f), "")
            for common_fraction in [0.5, 0.25, 0.75]:
                remainder = remainder.replace(str(common_fraction), "")

            if unit != "":
                if quantity > 1:
                    remainder = remainder.replace(unit_pluralized, "")
                else:
                    remainder = remainder.replace(unit, "")

            remainder = self._clean_string(remainder)

            words = remainder.split(" ")
            if len(words) == 1 and unit == "":
                remainder = ""
                unit = words[0]

            if unit == "pound-mass":
                unit = "pound"
            quantities.append((quantity, unit))

        if len(quantities) > 1 and (1, "") in quantities:
            quantities.remove((1, ""))
        return quantities, remainder


    def parse(self, original):
        s = self._clean_string(original)
        comment, s = self._get_comment(s)
        quantities, material = self._get_quantities(s)

        return {
            "original": original,
            "quantities": quantities,
            "comment": comment,
            "material": material,
        }


def _get_practice_ingredients(max_ingredients = 30):
    recipes = load_recipes()
    for id in recipes:
        ingredient_dict = recipes[id].get("ingredients", [])
        for ingredient_key in ingredient_dict:
            for ingredient in ingredient_dict[ingredient_key]:
                yield ingredient
                max_ingredients -= 1
                if max_ingredients <= 0:
                    return


if __name__ == "__main__":
    # ingredients = [
    #     '10 medium (blank)s tomatillos, husked',
    #     '1 small onion, chopped',
    #     '3 cloves garlic, chopped',
    #     '2 peppers jalapeno peppers, chopped',
    #     '1/4 cup chopped fresh cilantro',
    #     'salt and pepper to taste',
    #     '1 large turnip, peeled and cubed',
    #     '3 medium (blank)s white potatoes, peeled and cubed',
    #     '1/4 cup milk',
    #     '3 tablespoons unsalted butter',
    #     '1 teaspoon white sugar',
    #     '¾ teaspoon salt',
    #     '1/4 teaspoon pepper',
    #     '2 tablespoons chopped fresh rosemary',
    #     '4 garlic cloves, chopped, divided',
    #     '3 tablespoons olive oil, divided',
    #     '1 3.5–4-pound chicken, quartered',
    #     'Kosher salt, freshly ground pepper',
    #     '1 small shallot, finely chopped',
    #     '1 tablespoon fresh thyme leaves',
    #     '3/4 cup low-sodium chicken broth',
    #     '2 tablespoons unsalted butter, cut into pieces',
    #     '1 cup (2 sticks) unsalted butter, room temperature',
    #     '0.5 cup powdered sugar',
    #     '1 teaspoon freshly ground black pepper',
    #     '3/4 teaspoon kosher salt',
    #     '2 cups all-purpose flour plus more',
    #     '1 cup finely grated Parmesan (about 2 ounces)',
    #     '1 tablespoon fennel seeds',
    #     '1 teaspoon Maldon sea salt or other coarse salt',
    # ]
    p = Parser()
    for i in _get_practice_ingredients(500):
        response = p.parse(i)
        pprint.pprint(response)
        print()
        time.sleep(2)