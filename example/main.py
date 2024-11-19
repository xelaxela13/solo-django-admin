import os
from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from database import lifespan
from solo_django_admin.core.asgi import application

BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app_ = FastAPI(lifespan=lifespan)
    app_.mount(
        "/django-admin-static",
        StaticFiles(
            directory=os.path.join(BASE_DIR, "django_admin_static_files")),
        name="static",
    )
    app_.mount("/admin", application)

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    return app_


app = create_app()

if __name__ == '__main__':
    ...
