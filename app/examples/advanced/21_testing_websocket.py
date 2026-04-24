from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

app = FastAPI()


@app.get('/')
async def read_main():
    return {'message': 'hello world'}


@app.websocket('/ws')
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({'msg': 'hello websocket'})
    await websocket.close()


def test_read_main():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'hello world'}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect('/ws') as websocket:
        data = websocket.receive_json()
        assert data == {'msg': 'hello websocket'}
