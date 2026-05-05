from fastapi import APIRouter, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import AnalyticsServiceDep
from app.schemas.analytics import GroupAnalytics

router = APIRouter(prefix='/groups', tags=['Analytics'])


@router.get(
    '/{group_id}/analytics',
    response_model=GroupAnalytics,
    dependencies=[Security(get_current_user, scopes=['analytics:read'])],
)
async def get_group_analytics(
    group_id: int,
    service: AnalyticsServiceDep,
):
    return await service.get_group_analytics(group_id)
