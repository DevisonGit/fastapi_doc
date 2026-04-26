from fastapi import FastAPI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Awesome API'
    admin_email: str
    items_per_user: int = 50


settings = Settings()
app = FastAPI()


@app.get('/info')
async def info():
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user
    }


from fastapi import FastAPI

from ...config import settings


app = FastAPI()


@app.get('/info')
async def info():
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user
    }


from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from ...config_v2 import Settings


app = FastAPI()


@lru_cache
def get_settings():
    return Settings()

@app.get('/info')
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user
    }


from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from . import config_v3


app = FastAPI()


@lru_cache
def get_settings():
    return config_v3.Settings()

@app.get('/info')
async def info(
    settings: Annotated[config_v3.Settings, Depends(get_settings)]
):
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'items_per_user': settings.items_per_user
    }
