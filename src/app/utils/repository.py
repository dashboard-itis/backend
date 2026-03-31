from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class Repository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def get(self, obj_id: int) -> Optional[T]:
        result = await self.db.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None
    ) -> List[T]:

        query = select(self.model)

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)

        if search and search_fields:
            search_conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    search_conditions.append(column.ilike(f"%{search}%"))

            if search_conditions:
                query = query.where(func.or_(*search_conditions))

        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj_id: int, **kwargs) -> Optional[T]:
        obj = await self.get(obj_id)
        if not obj:
            return None

        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> Optional[T]:
        obj = await self.get(obj_id)
        if not obj:
            return None

        await self.db.delete(obj)
        await self.db.commit()
        return obj