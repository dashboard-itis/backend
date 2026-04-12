from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.stream import Stream
    from app.models.user import User
    from app.models.privacy_policy import PrivacyPolicy


class Group(BaseModel, table=True):
    __tablename__ = "groups"

    name: str = Field(index=True, unique=True, min_length=1, max_length=100)
    description: str | None = None

    users: list["User"] = Relationship(back_populates="group")
    streams: list["Stream"] = Relationship(back_populates="group")
    privacy_policy: "PrivacyPolicy | None" = Relationship(back_populates="group")