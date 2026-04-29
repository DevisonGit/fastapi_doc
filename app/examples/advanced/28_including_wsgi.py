from a2wsgi import WSGIMiddleware
from fastapi import FastAPI
from flask import Flask, request
from markupsafe import escape

flask_app = Flask(__name__)


@flask_app.route('/')
def flask_main():
    name = request.args.get('name', 'World')
    return f'hello,  {escape(name)} from Flask!'


app = FastAPI()


@app.get('/v2')
def read_main():
    return {'message': 'hello world'}


app.mount('/v1', WSGIMiddleware(flask_app))
