from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]