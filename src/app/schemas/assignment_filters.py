from typing import Optional

from app.schemas.base import CommonListFilters


class AssignmentFilters(CommonListFilters):
    title: Optional[str] = None
    course_id: Optional[int] = None
