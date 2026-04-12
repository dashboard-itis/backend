from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseSettings):
    db_schema: str = "postgresql+asyncpg"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "app_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return URL.create(
            drivername=self.db_schema,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)


class AppSettings(BaseSettings):
    app_name: str = "Academic Performance API"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Settings:
    def __init__(self) -> None:
        self.db = DatabaseSettings()
        self.app = AppSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()