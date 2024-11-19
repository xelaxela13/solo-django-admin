import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT", 5432)
    TORTOISE_DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
