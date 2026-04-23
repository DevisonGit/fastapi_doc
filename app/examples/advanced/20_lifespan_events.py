from contextlib import asynccontextmanager

from fastapi import FastAPI


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the ML model
    ml_models['answer_to_everything'] = fake_answer_to_everything_ml_model
    yield
    # clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get('/predict')
async def predict(x: float):
    print(ml_models)
    result = ml_models['answer_to_everything'](x)
    return {'result': result}


# deprecated
from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event('startup')
async def startup_event():
    items['foo'] = {'name': 'fighters'}
    items['bar'] = {'name': 'Tenders'}


@app.on_event('shutdown')
def shutdown_event():
    with open('log.txt', mode='a') as log:
        log.write('application shutdown')


@app.get('/items/{item_id}')
async def read_items(item_id: str):
    return items[item_id]
