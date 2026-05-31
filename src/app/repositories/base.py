from typing import Generic, TypeVar

from sqlalchemy import func
from sqlalchemy.sql import Select
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class Repository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get(self, object_id: int) -> T | None:
        return await self.session.get(self.model, object_id)

    async def fetch(
        self,
        filters: dict | None = None,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
    ) -> list[T]:
        query = select(self.model)
        query = self._apply_filters(query, filters=filters, search=search)
        query = query.offset(skip).limit(limit)

        result = await self.session.exec(query)
        return list(result.all())

    async def count(
        self,
        filters: dict | None = None,
        search: str | None = None,
    ) -> int:
        query = select(func.count()).select_from(self.model)
        query = self._apply_filters(query, filters=filters, search=search)

        result = await self.session.exec(query)
        return int(result.one())

    def _apply_filters(
        self,
        query: Select,
        filters: dict | None = None,
        search: str | None = None,
    ) -> Select:
        if filters:
            for field_name, value in filters.items():
                query = query.where(getattr(self.model, field_name) == value)

        if search and hasattr(self.model, 'name'):
            query = query.where(self.model.name.ilike(f'%{search}%'))

        return query

    async def create(self, **data) -> T:
        obj = self.model(**data)
        return await self.save(obj)

    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, object_id: int, **data) -> T | None:
        obj = await self.get(object_id)

        if obj is None:
            return None

        for field_name, value in data.items():
            setattr(obj, field_name, value)

        return await self.save(obj)

    async def delete(self, object_id: int) -> T | None:
        obj = await self.get(object_id)

        if obj is None:
            return None

        await self.session.delete(obj)
        await self.session.commit()

        return obj

    async def delete_by_filters(self, filters: dict) -> None:
        query = delete(self.model)

        for field_name, value in filters.items():
            query = query.where(getattr(self.model, field_name) == value)

        await self.session.exec(query)
        await self.session.commit()
