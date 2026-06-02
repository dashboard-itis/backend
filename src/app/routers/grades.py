from typing import Annotated

from fastapi import APIRouter, File, Query, Security, UploadFile, status
from fastapi.responses import Response

from app.core.error_responses import COMMON_ERROR_RESPONSES
from app.core.exceptions import BadRequestError, NotFoundError
from app.dependencies.auth import get_current_user
from app.dependencies.services import GradeServiceDep
from app.models.grade import GradeCreate, GradePublic, GradeUpdate
from app.schemas.base import PaginatedResponse
from app.schemas.grade import GradeImportResult, StudentGradeResponse

router = APIRouter(
    tags=['Grades'],
    responses=COMMON_ERROR_RESPONSES,
)


@router.get(
    '/grades',
    response_model=PaginatedResponse[StudentGradeResponse],
    dependencies=[Security(get_current_user, scopes=['grades:list'])],
)
async def get_grades(
    service: GradeServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return await service.get_all(skip=skip, limit=limit)


@router.post(
    '/grades/import',
    response_model=GradeImportResult,
    dependencies=[Security(get_current_user, scopes=['grades:create'])],
)
async def import_grades(
    service: GradeServiceDep,
    file: Annotated[UploadFile, File(...)],
):
    try:
        return await service.import_from_file(
            content=await file.read(),
            filename=file.filename or '',
        )
    except ValueError as exc:
        raise BadRequestError(str(exc)) from exc


@router.get(
    '/grades/export',
    dependencies=[Security(get_current_user, scopes=['grades:list'])],
)
async def export_grades(
    service: GradeServiceDep,
    student_id: Annotated[int | None, Query(ge=1)] = None,
    course_id: Annotated[int | None, Query(ge=1)] = None,
):
    content = await service.export_to_csv(
        student_id=student_id,
        course_id=course_id,
    )

    return Response(
        content=content,
        media_type='text/csv; charset=utf-8',
        headers={'Content-Disposition': 'attachment; filename="grades_export.csv"'},
    )


@router.get(
    '/grades/{grade_id}',
    response_model=StudentGradeResponse,
    dependencies=[Security(get_current_user, scopes=['grades:read'])],
)
async def get_grade(grade_id: int, service: GradeServiceDep):
    grade = await service.get_by_id(grade_id)

    if grade is None:
        raise NotFoundError('Grade not found')

    return grade


@router.post(
    '/grades',
    response_model=GradePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=['grades:create'])],
)
async def create_grade(grade_data: GradeCreate, service: GradeServiceDep):
    try:
        return await service.create(grade_data)
    except ValueError as exc:
        raise BadRequestError(str(exc)) from exc


@router.put(
    '/grades/{grade_id}',
    response_model=GradePublic,
    dependencies=[Security(get_current_user, scopes=['grades:update'])],
)
async def update_grade(
    grade_id: int,
    grade_data: GradeUpdate,
    service: GradeServiceDep,
):
    try:
        grade = await service.update(grade_id, grade_data)
    except ValueError as exc:
        raise BadRequestError(str(exc)) from exc

    if grade is None:
        raise NotFoundError('Grade not found')

    return grade


@router.delete(
    '/grades/{grade_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=['grades:delete'])],
)
async def delete_grade(grade_id: int, service: GradeServiceDep):
    deleted = await service.delete(grade_id)

    if not deleted:
        raise NotFoundError('Grade not found')


@router.get(
    '/students/{student_id}/grades',
    response_model=PaginatedResponse[StudentGradeResponse],
    dependencies=[Security(get_current_user, scopes=['grades:list'])],
)
async def get_student_grades(
    student_id: int,
    service: GradeServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return await service.get_student_grades(
        student_id=student_id,
        skip=skip,
        limit=limit,
    )
