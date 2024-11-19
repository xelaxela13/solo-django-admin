from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from settings import settings

MODELS = [
    "models.accounts",
    "models.companies"
]
TORTOISE_ORM = {
    "connections": {"default": settings.TORTOISE_DATABASE_URL},
    "apps": {
        "models": {
            "models": [*MODELS, "aerich.models"],
            "default_connection": "default",
        },
    },
}


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with RegisterTortoise(
            app,
            db_url=settings.TORTOISE_DATABASE_URL,
            modules={"models": MODELS},
            generate_schemas=True,
            add_exception_handlers=True,
    ):
        yield
    await Tortoise.close_connections()
