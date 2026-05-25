from typing import Optional

from app.schemas.base import CommonListFilters


class GradeFilters(CommonListFilters):
    student_id: Optional[int] = None
    course_id: Optional[int] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
