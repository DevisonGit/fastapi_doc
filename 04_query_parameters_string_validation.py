import random
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


# Query Additional validation
@app.get("/items/")
async def read_item(q: Annotated[str | None, Query( max_length=50)] = None):
    result = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        result.update({"q": q})
    return result


# More Additional validation
@app.get("/items/")
async def read_item(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None
):
    result = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        result.update({"q": q})
    return result


# Regular expressions
@app.get("/items/")
async def read_item(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None
):
    result = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        result.update({"q": q})
    return result


# Default values
@app.get("/items/")
async def read_item(q: Annotated[str, Query(min_length=3) ] = "fixedquery"):
    result = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        result.update({"q": q})
    return result


# Required Parameters
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


# Query parameters list
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


# Query parameters list multiples values with defaults
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


# list directly
@app.get("/items/")
async def read_items(q: Annotated[list, Query()] = []):
    query_items = {"q": q}
    return query_items


# Declare more metadata
@app.get("/items/")
async def read_items(
        q: Annotated[
            str | None,
            Query(
                title="Query String",
                description="Query string for the items"
            )] = None
):
    results = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


# Alias Parameters
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(alias="item-query")] = None
):
    results = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


# Deprecating parameters
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query String",
            description="Query string for the items to search in data base",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True
        )
    ] = None
):
    results = {"items": [{"item_id": "foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q": q})
    return results


# Exclude parameters from OpenAPI
@app.get("/items/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
    

# Custom validation
def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError(
            'Invalid ID format, it must start with "isbn- or "imdb-"'
        )
    return id


@app.get("/items/now")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
