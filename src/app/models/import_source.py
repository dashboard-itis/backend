from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.stream import Stream


class ImportSourceBase(SQLModel):
    stream_id: int | None = Field(default=None, foreign_key='streams.id')
    course_id: int | None = Field(default=None, foreign_key='courses.id')
    file_name: str = Field(min_length=1, max_length=255)
    uploaded_by: str = Field(min_length=1, max_length=255)
    status: str = Field(default='pending', min_length=1, max_length=50)


class ImportSource(ImportSourceBase, BaseModel, table=True):
    __tablename__ = 'import_sources'

    stream: Optional['Stream'] = Relationship(back_populates='import_sources')


class ImportSourceCreate(ImportSourceBase):
    pass


class ImportSourceUpdate(SQLModel):
    status: str | None = None


class ImportSourcePublic(ImportSourceBase, BaseModel):
    pass
