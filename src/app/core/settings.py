from datetime import timedelta
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class DatabaseSettings(BaseSettings):
    drivername: str = 'postgresql+asyncpg'
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    name: str = 'app_db'

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
    name: str = 'Dashboard ITIS'
    version: str = '1.0.0'
    description: str = 'API for academic performance analytics dashboard'
    servers: list[str] = ['http://localhost:8000']


class CORSSettings(BaseSettings):
    allow_origins: list[str] = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://localhost:8080',
    ]
    allow_credentials: bool = True
    allow_methods: list[str] = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
    allow_headers: list[str] = [
        'Accept',
        'Authorization',
        'Content-Type',
        'Origin',
        'X-Requested-With',
    ]
    max_age: int = 600


class RateLimitSettings(BaseSettings):
    default_limit: str = '100/minute'
    auth_limit: str = '10/minute'


class EmailSettings(BaseSettings):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str = 'smtp.gmail.com'
    mail_port: int = 587
    mail_from_name: str = 'Dashboard ITIS'
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True
    template_folder: str = 'app/templates/email'
    app_host: str = 'http://localhost:8000'
    confirmation_url: str = 'https://seccur.duckdns.org/confirm-account'
    confirmation_code_lifetime_minutes: int = 30


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str = 'HS256'
    access_token_lifetime: timedelta = timedelta(minutes=15)
    refresh_token_lifetime: timedelta = timedelta(days=30)


class RBACSettings(BaseSettings):
    admin_role: str = 'admin'
    public_role: str = 'public'
    student_role: str = 'student'
    curator_role: str = 'curator'


class AdminSettings(BaseSettings):
    email: str = 'admin@example.com'
    password: str = 'admin12345'
    first_name: str = 'Admin'
    last_name: str = 'User'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        extra='ignore',
    )

    db: DatabaseSettings
    app: AppSettings
    auth: AuthSettings
    rbac: RBACSettings
    admin: AdminSettings
    cors: CORSSettings
    rate_limit: RateLimitSettings
    email: EmailSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
