from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.groups import router as groups_router
from app.routers.courses import router as courses_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Academic Performance API...")
    yield
    print("Shutting down...")


app = FastAPI(
    title="Academic Performance API",
    version="1.0.0",
    lifespan=lifespan
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(groups_router)
api_router.include_router(courses_router)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Academic Performance API", "version": "1.0.0"}


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}