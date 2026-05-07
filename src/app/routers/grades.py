from typing import Annotated

from fastapi import APIRouter, Query, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import GradeServiceDep
from app.schemas.base import PaginatedResponse
from app.schemas.grade import StudentGradeResponse

router = APIRouter(prefix='/students', tags=['Grades'])


@router.get(
    '/{student_id}/grades',
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
