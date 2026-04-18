from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


# Declare header parameters
@app.get("/items")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}


# Automatic conversion
@app.get("/items/auto")
async def read_items(
    strange_header: Annotated[
        str | None, Header(convert_underscores=False)
    ] = None
):
    return {"strange_header": strange_header}


# Duplicate headers
@app.get("/items/duplicate/")
async def read_items(
    x_token: Annotated[list[str] | None, Header()] = None
):
    return {"X-Token values": x_token}
