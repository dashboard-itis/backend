from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CourseBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    stream_id: int
    teacher_id: int
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    stream_id: Optional[int] = None
    teacher_id: Optional[int] = None
    description: Optional[str] = None

class CoursePublic(CourseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True