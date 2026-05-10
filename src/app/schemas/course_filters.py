from pydantic import Field

from app.schemas.base import CommonListFilters


class CourseFilters(CommonListFilters):
    limit: int = Field(default=100, ge=1, le=100)
    name: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None
