from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


class CourseBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    stream_id: int | None = Field(default=None, foreign_key="streams.id")
    teacher_id: int | None = Field(default=None, foreign_key="users.id")


class Course(CourseBase, BaseModel, table=True):
    __tablename__ = "courses"

    stream: "Stream | None" = Relationship(back_populates="courses")
    teacher: "User | None" = Relationship(back_populates="courses")
    assignments: list["Assignment"] = Relationship(back_populates="course")
    grades: list["Grade"] = Relationship(back_populates="course")


class CourseCreate(CourseBase):
    pass


class CourseUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None


class CoursePublic(CourseBase, BaseModel):
    pass
