from typing import Annotated
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env", env_file_encoding="utf-8", extra='ignore')


class DatabaseConfig(BaseConfig):

    POSTGRES_USER: str = Field(alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(alias="POSTGRES_DB")
    POSTGRES_HOST: str = Field(alias="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(alias="POSTGRES_PORT")

    @property
    def postgresql_url(self) -> str:
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}'
              f':{self.POSTGRES_PORT}/{self.POSTGRES_DB}')


class AppConfig(BaseConfig):
    HOST: str = Field(alias="HOST")
    PORT: int = Field(alias="PORT")
    RELOAD: bool = Field(alias="RELOAD")
    ALLOWED_ORIGINS: Annotated[list[str], NoDecode] = Field(alias="ALLOWED_ORIGINS")

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def allowed_origins(cls, allowed_origins: str) -> list[str]:
        splited_origins = []

        for origins in allowed_origins.split(","):
            splited_origins.append(origins.strip())

        return splited_origins

    db: DatabaseConfig = Field(default_factory=DatabaseConfig)


settings = AppConfig()
