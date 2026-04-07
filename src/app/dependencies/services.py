from typing import Annotated

from fastapi import Depends

from app.dependencies.session import SessionDep
from app.services.course_service import CourseService
from app.services.group_service import GroupService
from app.services.user_service import UserService


async def get_user_service(db: SessionDep) -> UserService:
    return UserService(db)


async def get_group_service(db: SessionDep) -> GroupService:
    return GroupService(db)


async def get_course_service(db: SessionDep) -> CourseService:
    return CourseService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
GroupServiceDep = Annotated[GroupService, Depends(get_group_service)]
CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]