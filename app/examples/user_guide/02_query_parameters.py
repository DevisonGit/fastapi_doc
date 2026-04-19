from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resent = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_items_db = [{"items_name": "Foo"}, {"items_name": "Bar"}, {"items_name": "Baz"}]


# Query parameters
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 20):
    return fake_items_db[skip: skip + limit]


# Query Optional parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Query parameters type conversion
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# Required query parameters
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    return {"item_id": item_id, "needy": needy}


# parameters required, default value and optional
@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    return {
        "item_id": item_id, "needy": needy, "skip": skip, "limit": limit
    }
