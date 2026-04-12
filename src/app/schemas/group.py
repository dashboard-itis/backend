from datetime import datetime

from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class GroupPublic(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True