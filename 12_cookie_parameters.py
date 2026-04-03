from typing import Annotated

from fastapi import Cookie, FastAPI


app = FastAPI()


@app.get("/items/")
async def read_items(ads_is: Annotated[str | None, Cookie()] = None):
    return {"ads_is": ads_is}
