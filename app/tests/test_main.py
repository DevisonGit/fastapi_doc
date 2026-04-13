from fastapi import status
from fastapi.testclient import TestClient


from ..main import app

client = TestClient(app)


def test_read_main():
    response = client.get('/?token=jessica')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'hello bigger applications!'}


def test_read_main_invalid_token():
    response = client.get('/?token=jeh')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'No jessica token provided'}


def test_read_main_no_token():
    response = client.get('/')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

