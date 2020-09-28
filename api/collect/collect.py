#!/usr/bin/env python
from crawlers.allrecipes import AllRecipes
from crawlers.aseasyasapplepie import AsEasyAsApplePie
from utils import store_recipe, load_recipes, store_categories


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


def crawl():
    for crawler in [
        AllRecipes(),
        AsEasyAsApplePie(),
    ]:
        i = 0
        for recipe in crawler.next_recipe(skip_existing=True):
            i += 1
            if recipe is None:
                if i % 100 == 0:
                    print(i, "skipped")
                continue
            print(i, recipe.filename, recipe.title)
            store_recipe(recipe, overwrite=False)


if __name__ == "__main__":
    tree = build_category_tree()
    import pprint
    pprint.pprint(tree)
    crawl()
