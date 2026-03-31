from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_schema: str = "postgresql+asyncpg"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "adel"
    db_password: str = ""
    db_name: str = "app_db"

    app_name: str = "Academic Performance API"
    app_version: str = "1.0.0"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"{self.db_schema}://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()