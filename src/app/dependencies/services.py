from typing import Annotated

from fastapi import Depends

from app.services.course_service import CourseService
from app.services.group_service import GroupService
from app.services.user_service import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
GroupServiceDep = Annotated[GroupService, Depends(GroupService)]
CourseServiceDep = Annotated[CourseService, Depends(CourseService)]
