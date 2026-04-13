from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_users():
    response = client.get('/users/?token=jessica')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"username": "Rick"}, {"username": "Morty"}]


def test_read_users_invalid_token():
    response = client.get('/users/?token=invalid')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'No jessica token provided'}


def test_read_users_no_token():
    response = client.get('/users/')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_user_me():
    response = client.get('/users/me?token=jessica')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"username": "fakecurrentuser"}


def test_read_user_me_invalid_token():
    response = client.get('/users/me?token=invalid')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'No jessica token provided'}


def test_read_user_me_no_token():
    response = client.get('/users/me?')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_user():
    name = 'test'
    response = client.get(f'/users/{name}?token=jessica')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'username': name}


def test_read_user_invalid_token():
    response = client.get('/users/test?token=invalid')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'No jessica token provided'}


def test_read_user_no_token():
    response = client.get('/users/test?')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
