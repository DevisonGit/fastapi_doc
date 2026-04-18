from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# jsonable_encoder
fake_db = {}
app = FastAPI()


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    jsonable_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = jsonable_compatible_item_data


@app.get("/items/")
async def read_db():
    return fake_db
