from typing import Annotated

from fastapi import APIRouter, Query, Security

from app.core.error_responses import COMMON_ERROR_RESPONSES
from app.dependencies.auth import get_current_user
from app.dependencies.services import AnalyticsServiceDep
from app.schemas.analytics import GroupAnalytics, StudentAnalytics, TrendPeriod

router = APIRouter(
    prefix='',
    tags=['Analytics'],
    responses=COMMON_ERROR_RESPONSES,
)


@router.get(
    '/groups/{group_id}/analytics',
    response_model=GroupAnalytics,
    dependencies=[Security(get_current_user, scopes=['analytics:read'])],
)
async def get_group_analytics(
    group_id: int,
    service: AnalyticsServiceDep,
    trend_period: Annotated[TrendPeriod, Query()] = 'semester',
):
    return await service.get_group_analytics(group_id, trend_period)


@router.get(
    '/students/{student_id}/analytics',
    response_model=StudentAnalytics,
    dependencies=[Security(get_current_user, scopes=['analytics:read'])],
)
async def get_student_analytics(
    student_id: int,
    service: AnalyticsServiceDep,
    trend_period: Annotated[TrendPeriod, Query()] = 'semester',
):
    return await service.get_student_analytics(student_id, trend_period)
