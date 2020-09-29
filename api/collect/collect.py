#!/usr/bin/env python

from crawlers.allrecipes import AllRecipes
from crawlers.aseasyasapplepie import AsEasyAsApplePie
from crawlers.epicurious import Epicurious
from utils import store_recipe, load_recipes, store_categories, store_tags


def build_category_tree():

    def attach_to_tree(tree, categories):
        if len(categories) == 0:
            return tree
        category = categories[0]
        remaining = categories[1:]
        subtree = tree.get(category, {})
        subtree = attach_to_tree(subtree, remaining)
        tree[category] = subtree
        return tree

    def collapse_leaf_nodes(tree):
        contains_only_leaf = True
        for key in tree:
            if len(tree[key]) > 0:
                contains_only_leaf = False
                break

        if contains_only_leaf:
            return list(tree.keys())

        for key in tree:
            tree[key] = collapse_leaf_nodes(tree[key])
        return tree

    tree = {}
    recipes = load_recipes()
    for recipe in recipes.values():
        categories = recipe.get("category", [])
        if len(categories) > 0:
            print(categories)
            tree = attach_to_tree(tree, categories)
    tree = collapse_leaf_nodes(tree)
    store_categories(tree)

    return tree


def build_tags():
    results = {}
    recipes = load_recipes()
    for recipe in recipes.values():
        for tag in recipe.get("tags", []):
            if tag not in results:
                results[tag] = {
                    "count": 0,
                    "tag": tag
                }
            results[tag]["count"] += 1

    tags = list(results.values())
    store_tags(tags)
    return tags


def crawl():
    for crawler in [
        Epicurious(),
        AllRecipes(),
        AsEasyAsApplePie(),
    ]:
        i = 0
        for recipe in crawler.next_recipe(skip_existing=False):
            i += 1
            if recipe is None:
                if i % 100 == 0:
                    print(i, "skipped")
                continue
            print(
                crawler.domain,
                i,
                "\t",
                crawler.remaining,
                "\t",
                recipe.filename,
                recipe.title,
            )
            store_recipe(recipe, overwrite=True)


if __name__ == "__main__":
    # tree = build_category_tree()
    tags = build_tags()
    print(len(tags))
    crawl()
