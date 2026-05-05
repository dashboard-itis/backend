from datetime import datetime

from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.utcnow()


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={'server_default': func.now()},
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={
            'server_default': func.now(),
            'onupdate': func.now(),
        },
    )
