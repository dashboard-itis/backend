from sqlmodel import SQLModel


class CourseFilters(SQLModel):
    skip: int = 0
    limit: int = 100
    name: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None
    search: str | None = None
    