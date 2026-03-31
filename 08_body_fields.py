from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
     name: str
     description: str | None = Field(
          default=None, title="The descripition of the item", max_length=300,
     )
     price: float | None = Field(gt=0, title="The price must be greater than zero")
     tax: float | None = None

    
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
     return {"item_id": item_id, "item": item}
