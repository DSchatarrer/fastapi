# src\core\settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Literal
from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    PostgresDsn,
    Field
)
from pydantic_core import MultiHostUrl


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',  # <- Comenta o elimina esta línea para tomar las variables de entorno directamente
        env_file_encoding='utf-8', # <- Comenta o elimina esta línea para tomar las variables de entorno directamente
        extra="ignore",
        env_ignore_empty=True,
    )

    FASTAPI_SECRET_KEY: str
    FASTAPI_DEBUG: bool = False
    FASTAPI_DEBUG: bool = False
    FASTAPI_RUN_HOST: str = "0.0.0.0"
    FASTAPI_RUN_PORT: int = 8080
    
    JWT_SECRET_KEY: str
    ALGORITHM: str
    TOKEN_SECONDS_EXP: int
    API_KEY: str

    DATASOURCE_DB: str
    DATASOURCE_PORT: int
    DATASOURCE_FQDN: str
    DATASOURCE_USR: str
    DATASOURCE_PWD: str
    DATASOURCE_SCHEMA_SYNC: str
    DATASOURCE_SCHEMA_ASYNC: str

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = Field(default_factory=list)

    @computed_field
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DATASOURCE_FQDN}"
        return f"https://{self.DATASOURCE_FQDN}"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(MultiHostUrl.build(
            scheme=self.DATASOURCE_SCHEMA_SYNC,
            username=self.DATASOURCE_USR,
            password=self.DATASOURCE_PWD,
            host=self.DATASOURCE_FQDN,
            port=self.DATASOURCE_PORT,
            path=self.DATASOURCE_DB,
        ))
        
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI_ASYNC(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme=self.DATASOURCE_SCHEMA_ASYNC,
                username=self.DATASOURCE_USR,
                password=self.DATASOURCE_PWD,
                host=self.DATASOURCE_FQDN,
                port=self.DATASOURCE_PORT,
                path=f"{self.DATASOURCE_DB}",
            )
        )


settings = Settings()