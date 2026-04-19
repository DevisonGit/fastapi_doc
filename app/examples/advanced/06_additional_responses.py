from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class Message(BaseModel):
    message: str


app = FastAPI()


# additional response with model
@app.get(
    '/items/{item_id}',
    response_model=Item,
    responses={404: {'model': Message}}
)
async def read_item(item_id: str):
    if item_id == 'foo':
        return {'id': 'foo', 'value': 'there goes my hero'}
    return JSONResponse(status_code=404, content={'message': 'Item not found'})


# additional media types for the main response
@app.get(
    '/items/{item_id}',
    response_model=Item,
    responses={
        200: {
            'content': {'image/png': {}},
            'description': 'Return the JSON item or an image.'
        }

    }
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse('image.png', media_type='image/png')
    else:
        return {'id': 'foo', 'value': 'there goes my hero'}


# combining information
@app.get(
    '/items/{item_id}',
    response_model=Item,
    responses={
        404: {'model': Message, 'description': 'The item was not found'},
        200: {
            'content': {'application/json': {
                'example': {'id': 'foo', 'value': 'there goes my hero'}}
            },
            'description': 'Item requested by ID'
        }

    }
)
async def read_item(item_id: str):
    if item_id == 'foo':
        return {'id': 'foo', 'value': 'there goes my hero'}
    else:
        return JSONResponse(
            status_code=404,
            content={'message': 'item not found'}
        )


# combine predefined responses and custom ones
responses = {
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}


@app.get(
    '/items/{item_id}',
    response_model=Item,
    responses={**responses, 200: {'content': {'image/png': {}}}}
)
async def read_item(item_id: str, img: bool | None = None):
    if img:
        return FileResponse('image.png', media_type='image/png')
    else:
        return {'id': 'foo', 'value': 'there goes my hero'}
