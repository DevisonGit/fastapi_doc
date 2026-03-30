from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


# Declare metadata
@app.get("/items/{item_id}")
async def read_items(
   item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    return {"item_id": item_id}


# Number validations: greater than or equal
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The id of the item to get", ge=1)]
):
    return {"item_id": item_id}


# Number validations: greater than and less than or equal
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[float, Path(title="The ID of ther item to get", gt=0, le=1000)]
):
    return {"item_id": item_id}


# Number validations: floats, greater than and less than
@app.get("/items/{item_id}/now")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the to get", ge=1)],
    size: Annotated[float, Query(gt=0, lt=10.5)]
):
    return {"item_id": item_id, "size": size}
