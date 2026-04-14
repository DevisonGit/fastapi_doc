from typing import Annotated

from fastapi import Cookie, FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modifield_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


# Forbid extra Headers
class CommonHeadersForbid(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modifield_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers



@app.get("/items/forbid")
async def read_items(headers: Annotated[CommonHeadersForbid, Header(convert_underscores=False)]):
    return headers