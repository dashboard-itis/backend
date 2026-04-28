from typing import Annotated

from fastapi import Depends

from app.repositories.course_repository import CourseRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.refresh_session_repository import RefreshSessionRepository
from app.repositories.role_permission_repository import RolePermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository

UserRepositoryDep = Annotated[
    UserRepository,
    Depends(UserRepository),
]

GroupRepositoryDep = Annotated[
    GroupRepository,
    Depends(GroupRepository),
]

CourseRepositoryDep = Annotated[
    CourseRepository,
    Depends(CourseRepository),
]

RoleRepositoryDep = Annotated[
    RoleRepository,
    Depends(RoleRepository),
]

PermissionRepositoryDep = Annotated[
    PermissionRepository,
    Depends(PermissionRepository),
]

RolePermissionRepositoryDep = Annotated[
    RolePermissionRepository,
    Depends(RolePermissionRepository),
]

RefreshSessionRepositoryDep = Annotated[
    RefreshSessionRepository,
    Depends(RefreshSessionRepository),
]
