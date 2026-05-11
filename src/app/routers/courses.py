from typing import Annotated

from fastapi import APIRouter, Depends, Security, status

from app.core.error_responses import COMMON_ERROR_RESPONSES
from app.core.exceptions import NotFoundError
from app.dependencies.auth import get_current_user
from app.dependencies.services import CourseServiceDep
from app.models.course import CourseCreate, CoursePublic, CourseUpdate
from app.schemas.base import PaginatedResponse
from app.schemas.course_filters import CourseFilters

router = APIRouter(
    prefix='/courses',
    tags=['Courses'],
    responses=COMMON_ERROR_RESPONSES,
)

CourseFiltersDep = Annotated[CourseFilters, Depends()]


@router.get(
    '/',
    response_model=PaginatedResponse[CoursePublic],
    dependencies=[Security(get_current_user, scopes=['courses:list'])],
)
async def get_courses(
    service: CourseServiceDep,
    filters: CourseFiltersDep,
):
    return await service.get_all(filters)


@router.get(
    '/{course_id}',
    response_model=CoursePublic,
    dependencies=[Security(get_current_user, scopes=['courses:read'])],
)
async def get_course(course_id: int, service: CourseServiceDep):
    course = await service.get_by_id(course_id)

    if course is None:
        raise NotFoundError('Course not found')

    return course


@router.post(
    '/',
    response_model=CoursePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['courses:create'])],
)
async def create_course(
    course_data: CourseCreate,
    service: CourseServiceDep,
):
    return await service.create(course_data)


@router.put(
    '/{course_id}',
    response_model=CoursePublic,
    dependencies=[Security(get_current_user, scopes=['courses:update'])],
)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    service: CourseServiceDep,
):
    course = await service.update(course_id, course_data)

    if course is None:
        raise NotFoundError('Course not found')

    return course


@router.delete(
    '/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['courses:delete'])],
)
async def delete_course(course_id: int, service: CourseServiceDep):
    deleted = await service.delete(course_id)

    if not deleted:
        raise NotFoundError('Course not found')
