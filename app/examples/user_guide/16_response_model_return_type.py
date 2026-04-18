from typing import Any

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


# Return type
@app.post("/items/type")
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/type")
async def read_items() -> list[Item]:
    return [
        Item(name="portal gun", price=42.0),
        Item(name="pumblus", price=32.0)
    ]


# Response model
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        Item(name="portal gun", price=42.0),
        Item(name="pumblus", price=32.0)
    ]


# Return the same input data
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user


# Output model
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# Return type and data filtering
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@app.post("/users/base/")
async def create_user(user: UserIn) -> BaseUser:
    return user


# Other return type Annotations
@app.get("/portal/")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


# Annotate a Response Subclass
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# invalid return type annotations
# disable response model
@app.get("/portal/invalid/", response_model=None)
async def get_portal_invalid(teleport: bool = False) -> Response | str:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "here's your interdimensional portal."}


# Response model encoding parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] | None = None


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_items(item_id: str):
    return items[item_id]


# response_model_include response_model_exclude
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"}
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude={"tax"}
)
async def read_item_public_data(item_id: str):
    return items[item_id]
