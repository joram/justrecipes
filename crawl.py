#!/usr/bin/env python
import json
import os.path

from crawlers import interleaved_get_recipes
from db import Recipe as DBRecipe, Session, Ingredient, RecipeIngredient


def recipes_generator(load_existing=False):
    i = 0
    for head_recipe, url in interleaved_get_recipes():
        i += 1
        if head_recipe is None:
            continue

        # Skip existing
        if not load_existing:
            session = Session()
            qs = session.query(DBRecipe).filter(DBRecipe.pub_id == DBRecipe.get_pub_id(url))
            if len(qs.all()) != 0:
                yield qs.all()[0], True
                continue

        # Get new recipe
        recipe = DBRecipe.parse(head_recipe, url)
        if recipe is None:
            continue

        yield recipe, False


def crawl():
    print("starting crawl")
    i = 0
    for recipe, cached in recipes_generator():
        print(f"visited:{i} cached:{'T' if cached else 'F'} pub_id:{recipe.pub_id} \tdomain:{recipe.domain}\t recipe:{recipe.title}")
        if not cached:
            recipe.save(override=True)
        i += 1


def update_ingredients():
    session = Session()

    def get_ingredient_counts() -> dict:
        if os.path.exists("ingredient_counts.json"):
            with open("ingredient_counts.json") as f:
                return json.loads(f.read())
        ingredient_counts = {}
        qs = session.query(DBRecipe)
        i = 0
        for recipe in qs:
            i += 1
            for ingredient in recipe.detailed_ingredients:
                name = ingredient["name"]
                ingredient_counts[name] = ingredient_counts.get(name, 0) + 1
            if i % 100 == 0:
                print(f"{i}/{qs.count()}")
        with open("ingredient_counts.json", "w") as f:
            f.write(json.dumps(ingredient_counts))
        return ingredient_counts

    def get_sorted_ingredients():
        ingredient_counts = get_ingredient_counts()
        counts = list(set(ingredient_counts.values()))
        counts.sort(reverse=True)
        for val in counts:
            for name, count in ingredient_counts.items():
                if val == count and name != "":
                    yield name, count

    def top_10_ingredients():
        i = 1
        for name, count in get_sorted_ingredients():
            print(f"{count}\t{i}\t{name}")
            i += 1
            if i >= 11:
                break

    def update_ingredient_db():
        qs = session.query(DBRecipe)
        i = 0
        ingredient_counts = get_ingredient_counts()
        for recipe in qs:
            i += 1
            for ingredient in recipe.detailed_ingredients:
                name = ingredient["name"]

                if session.query(Ingredient).filter(
                    Ingredient.name == ingredient["name"],
                ).count() == 0:
                    Ingredient(name=name, count=ingredient_counts[name]).save()

                if session.query(RecipeIngredient).filter(
                    RecipeIngredient.recipe_pub_id == recipe.pub_id,
                    RecipeIngredient.ingredient_name == name,
                ).count() == 0:
                    ri = RecipeIngredient(recipe_pub_id=recipe.pub_id, ingredient_name=ingredient["name"])
                    ri.save()

            print(f"{i}/{qs.count()}")

    update_ingredient_db()


if __name__ == "__main__":
    # crawl()
    update_ingredients()
