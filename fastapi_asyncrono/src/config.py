# src\config.py

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This class defines the settings for the app
    """
    POSTGRES_URL: str
    ENVIRONMENT: str

    model_config = SettingsConfigDict(env_file=".env" if os.environ.get('ENVIRONMENT')=='Local' else None,
                                      extra="ignore")

settings = Settings()

print(settings.model_dump())

