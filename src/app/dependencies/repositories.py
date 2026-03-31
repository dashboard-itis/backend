from typing import Annotated
from fastapi import Depends
from app.dependencies.session import SessionDep
from app.utils.repository import Repository
from app.models.user import User
from app.models.group import Group
from app.models.course import Course


def get_user_repository(session: SessionDep):
    return Repository[User](session, User)


def get_group_repository(session: SessionDep):
    return Repository[Group](session, Group)


def get_course_repository(session: SessionDep):
    return Repository[Course](session, Course)


UserRepositoryDep = Annotated[Repository[User], Depends(get_user_repository)]
GroupRepositoryDep = Annotated[Repository[Group], Depends(get_group_repository)]
CourseRepositoryDep = Annotated[Repository[Course], Depends(get_course_repository)]