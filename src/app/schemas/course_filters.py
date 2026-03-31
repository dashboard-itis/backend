from typing import Optional
from app.schemas.base import CommonListFilters

class CourseFilters(CommonListFilters):
    name: Optional[str] = None
    stream_id: Optional[int] = None
    teacher_id: Optional[int] = None