from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient

items = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items['foo'] = {'name': 'fighters'}
    items['bar'] = {'name': 'tenders'}
    yield
    items.clear()


app = FastAPI(lifespan=lifespan)


@app.get('/items/{item_id}')
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    # before the lifespan starts, 'items' is still empty
    assert items == {}

    with TestClient(app) as client:
        # inside the 'with testclient' block, 
        # the lifespan starts and items added
        assert items == {
            'foo': {'name': 'fighters'}, 'bar': {'name': 'tenders'}
        }

        response = client.get('/items/foo')
        assert response.status_code == 200
        assert response.json() == {'name': 'fighters'}

        # After the requests is done, the items are still there
        assert items == {
            'foo': {'name': 'fighters'}, 'bar': {'name': 'tenders'}
        }

    # the end of the 'with TestClient' block simulates terminating the app, so
    # the lifespan ends and items are cleaned up
    assert items == {}


# deprecated
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

items = {}


@app.on_event('startup')
async def startup_event():
    items['foo'] = {'name': 'fighters'}
    items['bar'] = {'name': 'tenders'}


@app.get('/items/{item_id}')
async def read_items(item_id: str):
    return items[item_id]


def test_read_items():
    with TestClient(app) as client:
        response = client.get('/items/foo')
        assert response.status_code == 200
        assert response.json() ==  {'name': 'fighters'}