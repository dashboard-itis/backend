from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseModel):
    drivername: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    name: str = "app_db"

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


class AppSettings(BaseModel):
    name: str = "Dashboard ITIS"
    version: str = "1.0.0"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    app: AppSettings = Field(default_factory=AppSettings)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()