#!/usr/bin/env python
import math
import os

import flask as flask
import parse_ingredients
from flask import request
from flask_cors import CORS

from db.recipe import Session, Recipe, RecipeTag, Tag, Ingredient, RecipeIngredient
from sqlalchemy.orm import defer

global recipes, tags
app = flask.Flask(__name__, static_folder='./build')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v0/recipes')
def recipes_list():
    return flask.jsonify(list(recipes.keys()))


@app.route('/api/v0/recipes/search')
def recipes_search():
    session = Session()

    recipe_qs = session.query(Recipe).options(
        defer('url'),
        defer('title'),
        defer('ingredients'),
    )

    title = request.args.get('title')
    if title is not None and title != "undefined":
        recipe_qs = recipe_qs.filter(Recipe.title.like(f'%{title}%'))

    tag = request.args.get('tag')
    if tag is not None and tag != "undefined":
        qs = session.query(RecipeTag).filter(RecipeTag.tag_name == tag)
        recipe_pub_ids = [rt.recipe_pub_id for rt in qs.all()]
        recipe_qs = recipe_qs.filter(Recipe.pub_id.in_(recipe_pub_ids))

    ingredient = request.args.get('ingredient')
    if ingredient is not None and ingredient != "undefined":
        qs = session.query(RecipeIngredient).filter(RecipeIngredient.ingredient_name == ingredient)
        recipe_pub_ids = [ri.recipe_pub_id for ri in qs.all()]
        recipe_qs = recipe_qs.filter(Recipe.pub_id.in_(recipe_pub_ids))

    count = int(request.args.get('count', 10))
    page = int(request.args.get('page', 1))
    start = count*(page-1)
    end = count*page
    total = recipe_qs.count()
    recipe_qs = recipe_qs[start:end]

    results = {
        "recipes": [recipe.json() for recipe in recipe_qs],
        "total": total,
        "page": page,
        "page_count": math.ceil(total/count),
    }

    print(f"{total} recipes found, return page {page}/{int(total/count)}")
    return flask.jsonify(results)


meta_response = None


@app.route('/api/v0/meta')
def meta():
    global meta_response
    if meta_response is not None:
        return flask.jsonify(meta_response)
    session = Session()
    qs = session.query(Tag)
    tags = [{"tag": tag.name, "count": tag.count} for tag in qs.all() if tag.count >= 10]
    qs = session.query(Ingredient)
    ingredients = [{"ingredient": ingredient.name, "count": ingredient.count} for ingredient in qs.all() if ingredient.count >= 10]
    import pprint
    pprint.pprint(ingredients)

    meta_response = {
        "tags": tags,
        "ingredients": ingredients,
    }
    return flask.jsonify(meta_response)


@app.route('/api/v0/recipe/<pub_id>')
def recipe(pub_id):
    session = Session()
    qs = session.query(Recipe).filter(Recipe.pub_id == pub_id)
    if len(qs.all()) == 0:
        return flask.abort(404)
    recipe_json = qs.all()[0].json()

    from parse_ingredients import parse_ingredient
    detailed_ingredients = []
    for ingredient in recipe_json["ingredients"]:
        result = parse_ingredient(ingredient)
        detailed_ingredients.append({
            "name": result.name,
            "quantity": result.quantity,
            "unit": result.unit,
            "comment": result.comment,
            "original_string": result.original_string
        })
    recipe_json["ingredient_details"] = detailed_ingredients

    import pprint
    pprint.pprint(recipe_json)

    return flask.jsonify(recipe_json)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return flask.send_from_directory(app.static_folder, path)
    return flask.send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
