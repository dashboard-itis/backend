from typing import Generic, TypeVar

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class Repository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, object_id: int) -> T | None:
        return await self.session.get(self.model, object_id)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: dict | None = None,
        search: str | None = None,
    ) -> list[T]:
        query = select(self.model)

        if filters:
            for field_name, value in filters.items():
                query = query.where(getattr(self.model, field_name) == value)

        if search and hasattr(self.model, "name"):
            query = query.where(getattr(self.model, "name").ilike(f"%{search}%"))

        query = query.offset(skip).limit(limit)

        result = await self.session.exec(query)
        return list(result.all())

    async def create(self, **data) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, object_id: int, **data) -> T | None:
        obj = await self.get(object_id)
        if not obj:
            return None

        for field_name, value in data.items():
            setattr(obj, field_name, value)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, object_id: int) -> T | None:
        obj = await self.get(object_id)
        if not obj:
            return None

        await self.session.delete(obj)
        await self.session.commit()
        return obj