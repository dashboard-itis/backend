from typing import TYPE_CHECKING, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.base import BaseModel
from app.models.links import UserRoleLink

if TYPE_CHECKING:
    from app.models.attendance import Attendance
    from app.models.course import Course
    from app.models.grade import Grade
    from app.models.group import Group
    from app.models.refresh_session import RefreshSession
    from app.models.role import Role
    from app.models.submission import Submission


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    group_id: int | None = Field(default=None, foreign_key='groups.id')


class User(UserBase, BaseModel, table=True):
    __tablename__ = 'users'

    password_hash: str

    group: Optional['Group'] = Relationship(back_populates='users')
    courses: list['Course'] = Relationship(back_populates='teacher')
    grades: list['Grade'] = Relationship(back_populates='student')
    submissions: list['Submission'] = Relationship(back_populates='student')
    attendance_records: list['Attendance'] = Relationship(back_populates='student')
    refresh_sessions: list['RefreshSession'] = Relationship(back_populates='user')

    roles: list['Role'] = Relationship(
        back_populates='users',
        link_model=UserRoleLink,
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    group_id: int | None = None
    password: str | None = None


class UserPublic(UserBase, BaseModel):
    pass
