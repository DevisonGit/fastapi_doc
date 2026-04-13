from fastapi import status

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_update_admin():
    response = client.post(
        '/admin/?token=jessica',
        headers={'X-token': 'fake-super-secret-token'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ==  {'message': 'Admin getting schwifty'}


def test_update_admin_invalid_token():
    response = client.post(
        '/admin/?token=invalid',
        headers={'X-token': 'fake-super-secret-token'}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() ==  {'detail': 'No jessica token provided'}


def test_update_admin_invalid_x_token():
    response = client.post(
        '/admin/?token=jessica',
        headers={'X-token': 'invalid'}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() ==  {'detail': 'X-Token header invalid'}