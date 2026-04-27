from sqlmodel import SQLModel


class CommonListFilters(SQLModel):
    skip: int = 0
    limit: int = 100
    search: str | None = None


class CourseFilters(CommonListFilters):
    name: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None