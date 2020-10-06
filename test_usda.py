import os
from usda.client import UsdaClient
from dotenv import load_dotenv
load_dotenv()


client = UsdaClient(os.environ.get("USDA_API_KEY"))
foods = client.list_foods(5)
for food in foods:
    print(food.name)
