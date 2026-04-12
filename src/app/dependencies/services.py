from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import (
    CourseRepositoryDep,
    GroupRepositoryDep,
    UserRepositoryDep,
)
from app.services.course_service import CourseService
from app.services.group_service import GroupService
from app.services.user_service import UserService


def get_user_service(repo: UserRepositoryDep) -> UserService:
    return UserService(repo)


def get_group_service(repo: GroupRepositoryDep) -> GroupService:
    return GroupService(repo)


def get_course_service(repo: CourseRepositoryDep) -> CourseService:
    return CourseService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]
CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]