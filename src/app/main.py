from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.bootstrap.rbac import RBACBootstrapper
from app.db.database import AsyncSessionLocal
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.routers import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with AsyncSessionLocal() as session:
        bootstrapper = RBACBootstrapper(
            user_repo=UserRepository(session),
            role_repo=RoleRepository(session),
            permission_repo=PermissionRepository(session),
        )
        await bootstrapper.bootstrap()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
