from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseSettings):
    drivername: str = Field(default="postgresql+asyncpg", alias="DB_SCHEMA")
    host: str = Field(default="localhost", alias="DB_HOST")
    port: int = Field(default=5432, alias="DB_PORT")
    user: str = Field(default="postgres", alias="DB_USER")
    password: str = Field(default="postgres", alias="DB_PASSWORD")
    name: str = Field(default="app_db", alias="DB_NAME")

    model_config = SettingsConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def url(self) -> str:
        return URL.create(
            drivername=self.drivername,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)


class AppSettings(BaseSettings):
    name: str = Field(default="Dashboard ITIS", alias="APP_NAME")
    version: str = Field(default="1.0.0", alias="APP_VERSION")

    model_config = SettingsConfigDict(
        extra="ignore",
        populate_by_name=True,
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db: DatabaseSettings = DatabaseSettings()
    app: AppSettings = AppSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()