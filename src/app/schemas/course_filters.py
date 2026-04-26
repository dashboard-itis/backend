from typing import Annotated

from fastapi import Depends

from app.schemas.base import CommonListFilters


class CourseFilters(CommonListFilters):
    name: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None


CourseFiltersDep = Annotated[CourseFilters, Depends()]