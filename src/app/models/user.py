from enum import StrEnum

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel


class UserRole(StrEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    group_id: int | None = Field(default=None, foreign_key="groups.id")


class User(UserBase, BaseModel, table=True):
    __tablename__ = "users"

    password_hash: str
    role: UserRole = Field(default=UserRole.STUDENT)

    group: "Group | None" = Relationship(back_populates="users")
    courses: list["Course"] = Relationship(back_populates="teacher")
    grades: list["Grade"] = Relationship(back_populates="student")
    submissions: list["Submission"] = Relationship(back_populates="student")
    attendance_records: list["Attendance"] = Relationship(back_populates="student")


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = None


class UserPublic(UserBase, BaseModel):
    role: UserRole
