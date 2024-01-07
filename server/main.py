#!/usr/bin/env python3
from fastapi import FastAPI, Depends

from utils.jwt import get_jwt, get_email

CLIENT_ID = "184422986756-mneassqbhd7nsrbdmtbjcbped1kfi234.apps.googleusercontent.com"
app = FastAPI()

# in memory for now
PLANS = {}


@app.get("/plans")
async def get_plans(jwt=Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Getting plan ids for {email}")
    if email not in PLANS:
        PLANS[email] = {}

    return {"plan_ids": PLANS[email].keys()}


@app.post("/plan/{plan_id}/recipe")
async def add_recipe(plan_id: str, recipe_name:str, jwt=Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Adding {recipe_name} to {plan_id} for {email}")
    if email not in PLANS:
        PLANS[email] = {}
    if plan_id not in PLANS[email]:
        PLANS[email][plan_id] = []
    PLANS[email][plan_id].append(recipe_name)
    return {
        "plan_id": plan_id,
        "recipes": PLANS[email][plan_id]
    }


@app.delete("/plan/{plan_id}/recipe")
async def delete_recipe(plan_id: str, recipe_name:str, jwt = Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Removing {recipe_name} from {plan_id} for email {email}")
    if email not in PLANS:
        PLANS[email] = {}
    if plan_id not in PLANS[email]:
        PLANS[email][plan_id] = []
    PLANS[email][plan_id].remove(recipe_name)
    return {
        "plan_id": plan_id,
        "recipes": PLANS[email][plan_id]
    }

