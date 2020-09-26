#!/usr/bin/env python
import json

from flask import request
from flask_cors import CORS
import os

import flask as flask

recipes = {}
app = flask.Flask(__name__, static_folder='./build')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def load_recipes():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    recipes_path = os.path.join(dir_path, "../recipes/")
    for filename in os.listdir(recipes_path):
        filepath = os.path.join(recipes_path, filename)
        try:
            with open(filepath) as f:
                content = f.read()
                recipe = json.loads(content)
                uid = filename.replace(".json", "")
                recipes[uid] = recipe
                recipes[uid]["id"] = uid
        except:
            pass
    print(f"loaded {len(recipes)} recipes")


@app.route('/api/v0/recipes')
def recipes_list():
    return flask.jsonify(list(recipes.keys()))


@app.route('/api/v0/recipes/search')
def recipes_search():
    results = {}

    title = request.args.get('title')
    for recipe in recipes.values():
        if title in recipe.get("title"):
            results[recipe.get("title")] = recipe

    return flask.jsonify(list(results.values()))


@app.route('/api/v0/recipe/<pub_id>')
def recipe(pub_id):
    if pub_id not in recipes:
        return flask.abort(404)
    return flask.jsonify(recipes[pub_id])


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return flask.send_from_directory(app.static_folder, path)
    return flask.send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    load_recipes()
    app.run(host="0.0.0.0", debug=True)
