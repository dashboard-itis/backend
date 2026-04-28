from typing import Optional
from app.schemas.base import CommonListFilters

class SubmissionFilters(CommonListFilters):
    assignment_id: Optional[int] = None
    student_id: Optional[int] = None
    status: Optional[str] = None