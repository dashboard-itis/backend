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


class GradeImportError(BaseModel):
    row: int
    message: str


class GradeImportResult(BaseModel):
    created: int
    failed: int
    errors: list[GradeImportError] = []


class GradeExportItem(BaseModel):
    student_email: str
    student_last_name: str
    student_first_name: str
    group_id: int | None = None
    group_name: str | None = None
    course_name: str
    score: float
    comment: str | None = None
