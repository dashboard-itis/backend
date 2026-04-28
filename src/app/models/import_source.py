from sqlmodel import Field, SQLModel

from app.models.base import BaseModel


class ImportSourceBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    source_type: str = Field(min_length=1, max_length=100)
    description: str | None = None


class ImportSource(ImportSourceBase, BaseModel, table=True):
    __tablename__ = "import_sources"


class ImportSourceCreate(ImportSourceBase):
    pass


class ImportSourceUpdate(SQLModel):
    name: str | None = None
    source_type: str | None = None
    description: str | None = None


class ImportSourcePublic(ImportSourceBase, BaseModel):
    pass
