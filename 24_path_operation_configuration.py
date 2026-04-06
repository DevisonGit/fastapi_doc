from enum import Enum

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class User(BaseModel):
    username: str


# Response status code
@app.post("/items/", status_code=status.HTTP_201_CREATED, tags=["items"])
async def create_item(item: Item) -> Item:
    return item


# Tags
@app.get("/items/", tags=["items"])
async def read_item() -> list[Item]:
    return [{"name": "foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users() -> list[User]:
    return [{"username": "johndoe"}]


# Tags with enums
class Tags(Enum):
    items = "items"
    user = "users"


@app.get("/items/", tags=[Tags.items])
async def get_items() -> list:
    return ["portal", "plumbus"]


@app.get("/users/", tags=[Tags.user])
async def get_users() -> list:
    return ["rick", "morty"]


# Summary and description
@app.post(
    "/items/",
    summary="Create an Item",
    description="Create an item with all the information " \
    "name, description, price, tax and a set of unique tags"
)
async def create_item(item: Item) -> Item:
    return item


# Description form docstring
@app.post("/items/", summary="Create an Item")
async def create_item(item: Item) -> Item:
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tags strings for this item
    """
    return item


# Response description
@app.post(
        "/items/", 
        summary="Create an Item",
        response_description="The created item"
)
async def create_item(item: Item) -> Item:
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tags strings for this item
    """
    return item


# deprecate a path operation
@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_user():
    return [{"username": "foo"}]


@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item": "foo"}]
