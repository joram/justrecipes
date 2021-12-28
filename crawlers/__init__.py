from crawlers.allrecipes import AllRecipes
from crawlers.aseasyasapplepie import AsEasyAsApplePie
from crawlers.bon_appetit import BonAppetit
from crawlers.epicurious import Epicurious
from crawlers.ny_times import NYTimes
from crawlers.food_network import FoodNetwork
from crawlers.martha_stewart import MarthaStewart


def interleaved_get_recipes():
    crawlers = [
        Epicurious(),
        AllRecipes(),
        BonAppetit(),
        # AsEasyAsApplePie(),
        NYTimes(),
        FoodNetwork(),
        MarthaStewart(),
    ]
    next_recipes = [crawler.next_recipe() for crawler in crawlers]
    while len(next_recipes) > 0:
        for next_recipe in next_recipes:
            try:
                recipe, url = next_recipe.__next__()
                yield recipe, url
            except StopIteration:
                next_recipes = [f for f in next_recipes if f != next_recipe]
                break

