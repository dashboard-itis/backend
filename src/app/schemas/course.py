from datetime import datetime

from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    stream_id: int
    teacher_id: int
    description: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    stream_id: int | None = None
    teacher_id: int | None = None
    description: str | None = None


class CoursePublic(CourseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True