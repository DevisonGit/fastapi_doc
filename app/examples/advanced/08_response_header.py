from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/headers-and-object/')
async def get_headers(response: Response):
    response.headers['X-Cat-Dog'] = 'Alone in the world'
    return {'message': 'hello world'}


@app.get('/headers/')
def get_headers():
    content = {'message': 'Hello world'}
    headers = {'X-cat-dog': 'alone in the world', 'Content-language': 'en-US'}
    return JSONResponse(content=content, headers=headers)
