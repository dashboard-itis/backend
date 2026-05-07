from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class CommonListFilters(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
    search: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    skip: int
    limit: int
