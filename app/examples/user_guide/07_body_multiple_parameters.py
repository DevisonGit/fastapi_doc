from typing import Annotated

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


# Mix Path, Query And Body Parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price:  float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Multiple body parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    name: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}


# Singular values in Body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    name: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    return {"item_id": item_id, "item": item, "user": user, "importance": importance}


# Embed a single body parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}/now")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    return {"item_id": item_id, "item": item}
