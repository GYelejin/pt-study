from typing import Optional

from pydantic_settings import BaseSettings

from .db import DBSettings


class Settings(BaseSettings):
    # Type must be specified on fields that can be fetched from environment variables
    DEBUG: Optional[bool] = False

    # Project settings:
    PROJECT_NAME: Optional[str] = "Test app"
    FILES_BASE_PATH: Optional[str] = '/tmp'

    # Nested settings:
    DATABASE: DBSettings = DBSettings()


settings = Settings()
