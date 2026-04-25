from typing import Annotated

from fastapi import Depends, FastAPI, status
from fastapi.testclient import TestClient

app = FastAPI()


async def common_paremeters(
    q: str | None = None, skip: int = 0, limit: int = 0
):
    return {'q': q, 'skip': skip, 'limit': limit}


@app.get('/items/')
async def read_items(commons: Annotated[dict, Depends(common_paremeters)]):
    return {'message': 'hello items!', 'params': commons}


@app.get('/users/')
async def read_users(commons: Annotated[dict, Depends(common_paremeters)]):
    return {'message': 'hello users!', 'params': commons}


client = TestClient(app)


async def override_dependency(q: str | None = None):
    return {'q': q, 'skip': 5, 'limit': 10}


app.dependency_overrides[common_paremeters] = override_dependency


def test_override_in_items():
    response = client.get('/items/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'hello items!', 'params' :{
            'q': None, 'skip': 5, 'limit': 10
        }
    }


def test_override_in_items_with_q():
    response = client.get('/items/?q=foo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'hello items!', 'params' :{
            'q': 'foo', 'skip': 5, 'limit': 10
        }
    }


def test_override_in_items_with_parameters():
    response = client.get('/items/?q=foo&skip=100&limit=200')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'hello items!', 'params' :{
            'q': 'foo', 'skip': 5, 'limit': 10
        }
    }


def test_override_in_users():
    response = client.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'hello users!', 'params' :{
            'q': None, 'skip': 5, 'limit': 10
        }
    }


def test_override_in_users_with_q():
    response = client.get('/users/?q=foo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'hello users!', 'params' :{
            'q': 'foo', 'skip': 5, 'limit': 10
        }
    }


def test_override_in_users_with_parameters():
    response = client.get('/users/?q=foo&skip=100&limit=200')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'message': 'hello users!', 'params' :{
            'q': 'foo', 'skip': 5, 'limit': 10
        }
    }
    