from typing import Annotated

from fastapi import Depends

from app.schemas.course_filters import CourseFilters
from app.schemas.group_filters import GroupFilters
from app.schemas.user_filters import UserFilters

CourseFiltersDep = Annotated[CourseFilters, Depends()]
GroupFiltersDep = Annotated[GroupFilters, Depends()]
UserFiltersDep = Annotated[UserFilters, Depends()]
