from fastapi import APIRouter, FastAPI

from app.core.settings import settings
from app.routers.courses import router as courses_router
from app.routers.groups import router as groups_router
from app.routers.users import router as users_router

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(users_router)
api_router.include_router(groups_router)
api_router.include_router(courses_router)

app.include_router(api_router)


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}