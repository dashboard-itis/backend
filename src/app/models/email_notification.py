from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class EmailNotificationBase(SQLModel):
    action: str = Field(max_length=50, index=True)
    code: str = Field(max_length=100, index=True)
    user_id: int = Field(foreign_key='users.id', index=True)
    is_used: bool = Field(default=False, index=True)
    expires_at: datetime


class EmailNotification(EmailNotificationBase, BaseModel, table=True):
    __tablename__ = 'email_notifications'

    user: Optional['User'] = Relationship(back_populates='email_notifications')


class EmailNotificationCreate(EmailNotificationBase):
    pass


class EmailNotificationUpdate(SQLModel):
    is_used: bool | None = None


class EmailNotificationPublic(EmailNotificationBase, BaseModel):
    pass
