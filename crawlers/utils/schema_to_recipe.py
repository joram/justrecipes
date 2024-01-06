from typing import Optional

from bs4 import BeautifulSoup
from parse_ingredients import Ingredient as ParsedIngredient
from parse_ingredients import parse_ingredient

from .fda import ingredient_to_nutrients_infos
from recipes.models import Recipe, RecipeCategory, Ingredient


def _parse_categories(data):
    s = data.get("recipeCategory", "")
    if type(s) == str:
        s = [s]
    categories = []
    for category_string in s:
        for c in category_string.split(", "):
            try:
                RecipeCategory[c]
            except KeyError:
                continue
            categories.append(RecipeCategory[c])

    keywords = data.get("keywords", [])
    for keyword in keywords:
        try:
            RecipeCategory[keyword]
        except KeyError:
            continue
        categories.append(RecipeCategory[keyword])

    return categories


def _parse_servings(data):
    recipe_yield = data.get("recipeYield", "1")
    if type(recipe_yield) == list:
        recipe_yield = recipe_yield[0]
    if type(recipe_yield) == int:
        return recipe_yield
    servings = recipe_yield.lower()
    servings = servings.strip()
    words = servings.split(" ")
    numbers = []
    for word in words:
        try:
            numbers.append(int(word))
        except:
            pass
    if len(numbers) == 0:
        return None
    return int(sum(numbers)/len(numbers))


def _parse_minutes(data):
    s = data.get("totalTime")
    if s is None:
        return None
    s = s.lstrip("PDT")

    d = 0
    if "D" in s:
        parts = s.split("D")
        d = parts[0]
        s = parts[1]

    if "H" in s:
        parts = s.split("H")
        h = parts[0]
        m = parts[1].rstrip("M")
        if m == "":
            m = 0
        try:
            return int(d)*60*24 + int(h)*60 + int(m)
        except:
            return None

    if "M" in s:
        s = s.rstrip("M")
        try:
            return int(s)
        except:
            return None


def _parse_ingredients(data):
    ingredient_strings = data.get("recipeIngredient", data.get("recipeIngredients"))
    if ingredient_strings is None:
        return None
    ingredients = []
    for ingredient_string in ingredient_strings:
        ingredient_string = ingredient_string.lower()
        ingredient_string = ingredient_string.split(",")[0]
        ingredient_string = ingredient_string.split("and")[0]
        ingredient_string = ingredient_string.replace("/", " ", 1)
        for bad_word in ["optional", "plus more", "plus", "to taste", "(", ")"]:
            ingredient_string = ingredient_string.replace(bad_word, "")
        if "</" in ingredient_string:
            soup = BeautifulSoup(ingredient_string, 'html.parser')
            ingredient_string = soup.get_text()
        ingredient_string = ingredient_string.strip()

        ingredient_string = ingredient_string.replace("pinch", "a 1/4tsp")
        while "  " in ingredient_string:
            ingredient_string = ingredient_string.replace("  ", " ")

        substitute_words = {
            "¼": "1/4",
            "½": "1/2",
            "¾": "3/4",
            "⅓": "1/3",
            "⅔": "2/3",
            "⅛": "1/8",
            "⅜": "3/8",
            "⅝": "5/8",
            "⅞": "7/8",
            "⅕": "1/5",
            "⅖": "2/5",
            "⅗": "3/5",
            "⅘": "4/5",
        }
        for word, replacement in substitute_words.items():
            ingredient_string = ingredient_string.replace(word, replacement)

        is_a_seasoning = False
        seasonings = ["lemon", "parsely", "spray", "leaves", "ice", "salt", "pepper", "sugar", "cinnamon", "nutmeg", "cumin", "paprika", "chili powder", "chili flakes", "chili", "chile", "chiles", "chilies", "chili pepper", "chili peppers", "chile pepper", "chile peppers", "chili paste", "chile paste", "chili sauce", "chile sauce", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste", "chili powder", "chile powder", "chili flakes", "chile flakes", "chili oil", "chile oil", "chili sauce", "chile sauce", "chili paste", "chile paste"]
        for seasoning in seasonings:
            if seasoning in ingredient_string:
                is_a_seasoning = True
                break
        if is_a_seasoning:
            continue

        try:
            parsed_ingredient = parse_ingredient(ingredient_string)
        except Exception as e:
            parsed_ingredient = ParsedIngredient(
                name=ingredient_string,
                quantity=1,
                unit="",
                comment="",
                original_string=ingredient_string,
            )

        nutrients_infos = []
        ingredient = Ingredient(
            name=parsed_ingredient.name,
            amount=parsed_ingredient.quantity,
            unit=parsed_ingredient.unit,
            comment=parsed_ingredient.comment,
            nutrition_infos=nutrients_infos,
        )
        ingredients.append(ingredient)
    return ingredients


def _parse_instructions(data):
    instructions = data.get("recipeInstructions")
    if instructions is None:
        return None

    if isinstance(instructions[0], dict):
        return [inst["text"] for inst in instructions]

    return instructions


def _parse_notes(data):
    notes = data.get("recipeNotes")
    if notes is None:
        return []
    return notes


def _parse_images(data):
    image_details = data.get("image", [])
    if type(image_details) != list:
        image_details = [image_details]

    images = []
    for img in image_details:
        if type(img) == str:
            images.append(img)
        else:
            images.append(img.get("url"))
    return images


async def create_recipe(data, url) -> Optional[Recipe]:
    ingredients = _parse_ingredients(data)

    total_nutrition_infos = {}
    for ingredient in ingredients:
        ingredient.nutrition_infos = await ingredient_to_nutrients_infos(ingredient)
        for nutrient in ingredient.nutrition_infos:
            if nutrient.name not in total_nutrition_infos:
                total_nutrition_infos[nutrient.name] = nutrient
            else:
                total_nutrition_infos[nutrient.name].amount += nutrient.amount

    def _to_recipe():
        return Recipe(
            name=data.get("name", ""),
            categories=_parse_categories(data),
            servings=_parse_servings(data),
            minutes=_parse_minutes(data),
            source_url=url,
            image_urls=_parse_images(data),
            ingredients=ingredients,
            instructions=_parse_instructions(data),
            notes=_parse_notes(data),
            nutrition_infos=total_nutrition_infos.values(),
        )

    try:
        return _to_recipe()
    except Exception as e:
        print(f"Error creating recipe for {url}")
        print(e)
        return None
