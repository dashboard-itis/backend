from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import IdModel, TimestampedModel

if TYPE_CHECKING:
    from app.models.privacy_policy import PrivacyPolicy
    from app.models.stream import Stream
    from app.models.user import User


class GroupBase(SQLModel):
    name: str = Field(index=True, unique=True, min_length=1, max_length=100)
    description: str | None = None


class Group(GroupBase, IdModel, TimestampedModel, table=True):
    __tablename__ = "groups"

    users: list["User"] = Relationship(back_populates="group")
    streams: list["Stream"] = Relationship(back_populates="group")
    privacy_policy: "PrivacyPolicy | None" = Relationship(back_populates="group")


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class GroupPublic(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime