import enum
from typing import List, Optional

from pydantic import BaseModel


class NutritionalInfo(BaseModel):
    name: str
    amount: float
    unit: str
    serving_size: float
    serving_size_unit: str


class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str
    comment: str
    nutrition_infos: List[NutritionalInfo]


class RecipeCategory(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    DESSERT = "dessert"
    SNACK = "snack"
    DRINK = "drink"
    OTHER = "other"
    STARTER = "starter"
    NUT_FREE = "nut free"
    GLUTEN_FREE = "gluten free"
    MAKE_AHEAD = "make ahead"
    OVEN_BAKE = "oven bake"
    GOURMET = "gourmet"


class Recipe(BaseModel):
    name: str
    categories: List[RecipeCategory]
    servings: Optional[int]
    minutes: Optional[int]

    source_url: str
    image_urls: List[str]
    ingredients: List[Ingredient]
    instructions: List[str]
    notes: List[str]

    nutrition_infos: List[NutritionalInfo]
