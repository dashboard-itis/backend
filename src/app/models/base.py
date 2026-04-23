from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column_kwargs={"onupdate": utc_now},
    )


class IdModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class BaseTableModel(IdModel, TimestampedModel):
    pass