from fastapi import FastAPI, Request

app = FastAPI(root_path='/api/v1')


@app.get('/items/')
def read_items():
    return ['plumbus', 'portal gun']


@app.get('/app')
def read_main(request: Request):
    return {
        'message': 'hello world',
        'root_path': request.scope.get('root_path')
    }


app = FastAPI(
    servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"},
    ],
    root_path='/api/v1',
    root_path_in_servers=False
)


@app.get('/app')
def read_main(request: Request):
    return {
        'message': 'hello world', 'root_path': request.scope.get('root_path')
        }
