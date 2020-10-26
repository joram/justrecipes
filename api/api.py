#!/usr/bin/env python
import copy
import os

import flask as flask
from flask import request
from flask_cors import CORS

from utils import load_recipes, load_tags

from db.recipe import Session, Recipe, RecipeTag, Tag
from ingredients.parse import Parser

global recipes, tags
app = flask.Flask(__name__, static_folder='./build')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v0/recipes')
def recipes_list():
    return flask.jsonify(list(recipes.keys()))


@app.route('/api/v0/recipes/search')
def recipes_search():
    session = Session()

    title = request.args.get('title')
    if title is not None:
        qs = session.query(Recipe).filter(Recipe.title.like(f'%{title}%'))
        results = [recipe.json() for recipe in qs.all()]
        print(f"{len(results)} recipes found")
        return flask.jsonify(results)

    tag = request.args.get('tag')
    if tag is not None:
        qs = session.query(RecipeTag).filter(RecipeTag.tag_name == tag)
        recipe_pub_ids = [rt.recipe_pub_id for rt in qs.all()]
        qs = session.query(Recipe).filter(Recipe.pub_id.in_(recipe_pub_ids))
        results = [recipe.json() for recipe in qs.all()]
        print(f"{len(results)} recipes found")
        return flask.jsonify(results)


@app.route('/api/v0/meta')
def meta():
    session = Session()
    qs = session.query(Tag)
    tags = [{"tag": tag.name, "count": tag.count} for tag in qs.all()]
    response = {
        "tags": tags,
    }
    return flask.jsonify(response)


@app.route('/api/v0/recipe/<pub_id>')
def recipe(pub_id):
    session = Session()
    qs = session.query(Recipe).filter(Recipe.pub_id == pub_id)
    if len(qs) == 0:
        return flask.abort(404)
    recipe_json = qs.all()[0].json()

    parser = Parser()
    for key in recipe_json["ingredients"]:
        ingredients = []
        for ingredient in recipe_json["ingredients"][key]:
            ingredients.append(parser.parse(ingredient))
        recipe_json["ingredients"][key] = ingredients

    def get_original_image(d):
        if "originals" in d["originals"]:
            return get_original_image(d["originals"])
        return d["originals"]

    recipe_json["images"]["originals"] = get_original_image(recipe_json["images"]["originals"])

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
