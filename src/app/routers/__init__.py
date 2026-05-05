from fastapi import APIRouter

from app.routers import analytics, auth, courses, grades, groups, users

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(groups.router)
api_router.include_router(courses.router)
api_router.include_router(analytics.router)
api_router.include_router(grades.router)
