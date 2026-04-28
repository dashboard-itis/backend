from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class RefreshSessionBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    access_token_jti: str = Field(
        index=True,
        unique=True,
        min_length=1,
        max_length=100,
    )
    refresh_token_jti: str = Field(
        index=True,
        unique=True,
        min_length=1,
        max_length=100,
    )
    expires_at: datetime
    is_invalidated: bool = False


class RefreshSession(RefreshSessionBase, BaseModel, table=True):
    __tablename__ = "refresh_sessions"

    user: Optional["User"] = Relationship(back_populates="refresh_sessions")

    @property
    def is_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        return not self.is_invalidated and self.expires_at > now


class RefreshSessionCreate(RefreshSessionBase):
    pass


class RefreshSessionUpdate(SQLModel):
    is_invalidated: bool | None = None


class RefreshSessionPublic(RefreshSessionBase, BaseModel):
    pass
