from datetime import datetime

from pydantic import BaseModel


class StudentGradeResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    score: float
    comment: str | None = None
    created_at: datetime
    updated_at: datetime
    course_name: str | None = None
