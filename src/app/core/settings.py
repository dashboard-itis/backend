from functools import lru_cache

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseModel):
    drivername: str
    host: str
    port: int
    user: str
    password: str
    name: str

    @computed_field
    @property
    def database_url(self) -> str:
        return URL.create(
            drivername=self.drivername,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)


class AppSettings(BaseModel):
    name: str
    version: str


class Settings(BaseSettings):
    db_schema: str = "postgresql+asyncpg"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "app_db"

    app_name: str = "Academic Performance API"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(
            drivername=self.db_schema,
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            name=self.db_name,
        )

    @property
    def app(self) -> AppSettings:
        return AppSettings(
            name=self.app_name,
            version=self.app_version,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()