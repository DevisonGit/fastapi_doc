from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_items():
    response = client.get(
        '/items/?token=jessica',
        headers={'X-token': 'fake-super-secret-token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}
        }


def test_read_items_invalid_token():
    response = client.get(
        '/items/?token=invalid',
        headers={'X-token': 'fake-super-secret-token'}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'No jessica token provided'}


def test_read_items_invalid_x_token():
    response = client.get(
        '/items/?token=jessica',
        headers={'X-token': 'invalid'}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'X-Token header invalid'}


def test_read_items_no_token():
    response = client.get(
        '/items/?',
        headers={'X-token': 'fake-super-secret-token'}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_items_no_x_token():
    response = client.get(
        '/items/?token=jessica',
        headers={}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_item():
    item = 'plumbus'
    response = client.get(
        f'/items/{item}?token=jessica',
        headers={'X-token': 'fake-super-secret-token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'name': 'Plumbus', 'item_id': item}


def test_update_item():
    item = 'plumbus'
    response = client.put(
        f'/items/{item}?token=jessica',
        headers={'X-token': 'fake-super-secret-token'},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'item_id': item, 'name': 'The great plumbus'}


def test_update_item_gun():
    response = client.put(
        '/items/gun?token=jessica',
        headers={'X-token': 'fake-super-secret-token'},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        'detail': 'you can only update the item: plumbus'
    }
