from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


items = {"foo": "The Foo Wrestlers"}


# raise HTTPException
@app.get("/items/{item_id}")
async def reat_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item not found")
    return {"item": items[item_id]}


# Add custom headers
@app.get("/items-header/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}


# Custon exception handlers
@app.exception_handler(UnicornException)
async def unicor_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow."
            }
    )


@app.get("/unicors/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# Override the default exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't  like 3")
    return {"item_id": item_id}


# use RequestValidationError
@app.exception_handler(RequestValidationError)
async def validation_exception_hendler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )


class Item(BaseModel):
    name: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item

# Reuse FastAPI exception handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data! {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}