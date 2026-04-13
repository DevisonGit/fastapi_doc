from fastapi import status
from fastapi.testclient import TestClient


from ..main import app

client = TestClient(app)

def test_read_item():
    response = client.get(
        '/items/foo',
        headers={'x-token': 'coneofsilence'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": "foo", "title": "Foo", "description": "There goes my hero"
        }
    
def test_read_item_bad_token():
    response = client.get('/items/foo', headers={'x-token': 'heilhydra'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'invalid X-Token header'}


def test_read_nonexistent_item():
    response = client.get('/items/baz', headers={'X-token': 'coneofsilence'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_create_item():
    response = client.post(
        '/items/',
        headers={'X-token': 'coneofsilence'},
        json={
            "id": "foobar", 
            "title": "Foo Bar", 
            "description": "The Foo Barters"
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
            "id": "foobar", 
            "title": "Foo Bar", 
            "description": "The Foo Barters"
        }


def test_create_item_bad_token():
    response = client.post(
        '/items/',
        headers={'X-token': 'heilhydra'},
        json={
            "id": "foobar", 
            "title": "Foo Bar", 
            "description": "The Foo Barters"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'invalid X-Token header'}


def test_create_existing_item():
    response = client.post(
        '/items/',
        headers={'X-token': 'coneofsilence'},
        json={
            "id": "foo", 
            "title": "Foo", 
            "description": "There goes my hero"
        }
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Item already exists'}
    