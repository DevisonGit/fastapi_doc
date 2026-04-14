from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

# Dependency injection
async def common_parameters(
        q: str | None = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


# sharing Annotated dependencies
async def common_parameters(
        q: str | None = None, skip: int = 0,  limit: int = 100
):
    return {"q": q, 'skip': skip, 'limit': limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons


@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
