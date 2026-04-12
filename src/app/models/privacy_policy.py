from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.group import Group


class PrivacyPolicy(BaseModel, table=True):
    __tablename__ = "privacy_policies"

    group_id: int = Field(foreign_key="groups.id", unique=True)
    show_rating_to_students: bool = Field(default=True)
    rating_mode: str = Field(default="anonymized")
    allow_student_stats: bool = Field(default=True)
    version: int = Field(default=1, ge=1)

    group: "Group | None" = Relationship(back_populates="privacy_policy")