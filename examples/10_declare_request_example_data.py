from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


# Extra JSON Schema data
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra":{
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            ]
        }
    }


# Field additional arguments
class Item(BaseModel):
    name: str = Field(examples=["foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}


# Body with examples
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            ]

        )
    ]
):
    return {"item_id": item_id, "item": item}


# Body with multiple examples
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                },
                {
                    "name": "Foo",
                    "price": 35.4,
                }
            ]
        )
    ]
):
    return {"item_id": item_id, "item": item}


# OpenAPI specific examples
@app.put("/items/{item_id}/now")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2
                    }
                },
                "converted":{
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price 'strings' to actual 'numbers' automatically",
                    "value": {
                        "name": "Foo",
                        "price": "35.4"
                    }
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Foo",
                        "price": "thirty five point four"
                    }
                }
            }
        )
    ]
):
    return {"item_id": item_id, "item": item}