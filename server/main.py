#!/usr/bin/env python3
from typing import Union

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, BaseModel
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from mangum import Mangum

from utils.jwt import get_jwt, get_email

CLIENT_ID = "184422986756-mneassqbhd7nsrbdmtbjcbped1kfi234.apps.googleusercontent.com"
app = FastAPI(middleware=[
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
])

# in memory for now
PLANS = {}


@app.get("/plans")
async def get_plans(jwt=Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Getting plan ids for {email}")
    if email not in PLANS:
        PLANS[email] = {}

    return {"plan_ids": PLANS[email].keys()}


@app.get("/plan/{plan_id}")
async def get_plan(plan_id:str, jwt=Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Getting plan {plan_id} for {email}")
    if email not in PLANS:
        PLANS[email] = {}
    if plan_id not in PLANS[email]:
        PLANS[email][plan_id] = []
    return {
        "plan_id": plan_id,
        "recipes": PLANS[email][plan_id]
    }


class RecipeNameRequest(BaseModel):
    recipe_name: str


@app.post("/plan/{plan_id}/recipe")
async def add_recipe(plan_id: str, request: RecipeNameRequest, jwt=Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Adding {request.recipe_name} to {plan_id} for {email}")
    if email not in PLANS:
        PLANS[email] = {}
    if plan_id not in PLANS[email]:
        PLANS[email][plan_id] = []
    PLANS[email][plan_id].append(request.recipe_name)
    return {
        "plan_id": plan_id,
        "recipes": PLANS[email][plan_id]
    }


@app.delete("/plan/{plan_id}/recipe")
async def delete_recipe(plan_id: str, request: RecipeNameRequest, jwt = Depends(get_jwt)):
    email = get_email(jwt)
    print(f"Removing {request.recipe_name} from {plan_id} for email {email}")
    if email not in PLANS:
        PLANS[email] = {}
    if plan_id not in PLANS[email]:
        PLANS[email][plan_id] = []
    PLANS[email][plan_id].remove(request.recipe_name)
    return {
        "plan_id": plan_id,
        "recipes": PLANS[email][plan_id]
    }


async def http422_error_handler(
    _, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    print(_.json())
    return JSONResponse(
        {"errors": exc.errors()}, status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )

app.add_exception_handler(ValidationError, http422_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

handler = Mangum(app)
