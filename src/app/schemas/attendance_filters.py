from typing import Optional
from app.schemas.base import CommonListFilters

class AttendanceFilters(CommonListFilters):
    course_id: Optional[int] = None
    student_id: Optional[int] = None
    status: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None