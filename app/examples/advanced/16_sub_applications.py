from fastapi import FastAPI

app = FastAPI()


@app.get('/app')
async def read_main():
    return {'message': 'hello world from main app'}


subapi = FastAPI()

@subapi.get('/sub')
async def read_sub():
    return {'message': 'hello world from sub API'}


app.mount('/subapi', subapi)
