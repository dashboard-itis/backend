from datetime import date, datetime, timezone

from typing import Optional



from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    email: str = Field(index=True)
    password_hash: str
    first_name: str
    last_name: str
    role: str

    group_id: int | None = Field(default=None, foreign_key='group.id')

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(index=True)
    year: int
    description: str | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Stream(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    group_id: int = Field(foreign_key='group.id')
    semester: int
    year: int


class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    stream_id: int = Field(foreign_key='stream.id')
    teacher_id: int = Field(foreign_key='user.id')

    name: str
    description: str | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Assignment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    course_id: int = Field(foreign_key='course.id')

    title: str
    max_score: float
    weight: float | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Grade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    assignment_id: int = Field(foreign_key='assignment.id')
    student_id: int = Field(foreign_key='user.id')

    score: float
    comment: str | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Submission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    assignment_id: int = Field(foreign_key='assignment.id')
    student_id: int = Field(foreign_key='user.id')

    status: str
    submitted_at: datetime | None = None


class Attendance(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    course_id: int = Field(foreign_key='course.id')
    student_id: int = Field(foreign_key='user.id')

    date: date
    status: str


class PrivacyPolicy(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    group_id: int = Field(foreign_key='group.id')

    show_rating_to_students: bool
    rating_mode: str
    allow_student_stats: bool
    version: int

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ImportSource(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    stream_id: int = Field(foreign_key='stream.id')
    course_id: int = Field(foreign_key='course.id')

    file_name: str
    uploaded_by: str
    status: str


    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



