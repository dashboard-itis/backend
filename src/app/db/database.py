from typing import Annotated
from fastapi import Depends
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.settings import settings

Base = declarative_base()

def get_database_url() -> str:
    return URL.create(
        drivername=settings.db_schema,
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    ).render_as_string(hide_password=False)


engine = create_async_engine(
    get_database_url(),
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]