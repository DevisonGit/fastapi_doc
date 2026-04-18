from typing import Any

import anyio
import orjson
from fastapi import FastAPI, Response
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
)

app = FastAPI()


# HTML Response
@app.get('/items', response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


# Return Response
@app.get('/items')
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get('/items/', response_class=HTMLResponse)
async def read_items():
    return generate_html_response()


@app.get('/legacy/')
async def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type='application/xml')


# PlainTextResponse
@app.get('/', response_class=PlainTextResponse)
async def main():
    return 'hello world'


# RedirectResponse
@app.get('/typer')
async def redirect_typer():
    return RedirectResponse('https://typer.tiangolo.com')


@app.get('/fastapi', response_class=RedirectResponse)
async def redirect_fastapi():
    return 'https://fastapi.tiangolo.com'


@app.get('/pydantic', response_class=RedirectResponse, status_code=302)
async def redirect_pydantic():
    return 'https://docs.pydantic.dev/'


# StreamingResponse
async def fake_video_streamer():
    for i in range(10):
        yield b'some fake video bytes'
        await anyio.sleep(1)


@app.get('/')
async def main():
    return StreamingResponse(fake_video_streamer())


# FileResponse
some_file_path = 'large-video-file.mp4'


@app.get('/')
async def main():
    return FileResponse(some_file_path)


@app.get('/', response_class=FileResponse)
async def main():
    return some_file_path


# custom response class
class CustomORJSONResponse(Response):
    media_type = 'application/json'

    def render(self, content: Any) -> bytes:
        assert orjson is not None, 'orjson must be installed'
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


@app.get('/', response_class=CustomORJSONResponse)
async def main():
    return {'message': 'hello world'}


# default response class
app = FastAPI(default_response_class=HTMLResponse)


@app.get('/items/')
async def read_items():
    return "<h1>Items</h1><p>This is a list of items.</p>"
