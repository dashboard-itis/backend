from typing import Annotated

from fastapi import Depends

from app.services.analytics_service import AnalyticsService
from app.services.auth_service import AuthService
from app.services.course_service import CourseService
from app.services.email_service import EmailService
from app.services.grade_service import GradeService
from app.services.group_service import GroupService
from app.services.user_service import UserService

UserServiceDep = Annotated[UserService, Depends(UserService)]
GroupServiceDep = Annotated[GroupService, Depends(GroupService)]
CourseServiceDep = Annotated[CourseService, Depends(CourseService)]
AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
AnalyticsServiceDep = Annotated[AnalyticsService, Depends(AnalyticsService)]
GradeServiceDep = Annotated[GradeService, Depends(GradeService)]
EmailServiceDep = Annotated[EmailService, Depends(EmailService)]
