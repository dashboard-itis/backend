from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class IdModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class TimestampedModel(SQLModel):
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class BaseTableModel(IdModel, TimestampedModel):
    pass


class BaseModel(IdModel, TimestampedModel):
    pass
