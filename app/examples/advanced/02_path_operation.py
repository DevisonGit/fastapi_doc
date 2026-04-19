import yaml
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.routing import APIRoute
from pydantic import BaseModel, ValidationError

app = FastAPI()


# OpenAPI operationId
@app.get('/items/', operation_id='some_specific_id_you_define')
async def read_items():
    return [{'item_id': 'foo'}]


# Using path operation function names as the operationId
@app.get('/items/')
async def read_items():
    return [{'item_id': 'foo'}]


def user_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


user_route_names_as_operation_ids(app)


# exclude from OpenAPI
@app.get('/items/', include_in_schema=False)
async def read_items():
    return [{'item_id': 'foo'}]


# Advanced description from docstring
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post('/items/', summary='create an Item')
async def read_items(item: Item) -> Item:
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return item


# OpenAPI Extensions
@app.get('/items/', openapi_extra={'x-aperture-labs-portal': 'blue'})
async def read_items():
    return [{'item_id': 'portal-gun'}]


# Custom OpenAPI path operation schema
def magic_data_reader(raw_body: bytes):
    return {
        "size": len(raw_body),
        "content": {
            "name": "Maaaagic",
            "price": 42,
            "description": "Just kiddin', no magic here. ✨",
        },
    }


@app.post(
    '/items/',
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": {
                        "required": ["name", "price"],
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"},
                        },
                    }
                }
            },
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    data = magic_data_reader(raw_body)
    return data


# Custom OpenAPI content type
class Item(BaseModel):
    name: str
    tags: list[str]


@app.post(
    '/items/',
    openapi_extra={
        "requestBody": {
            "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
            "required": True,
        },
    },
)
async def create_item(request: Request):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Invalid YAML'
        )
    try:
        item = Item.model_validate(data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=e.errors(include_url=False)
        )
    return item
