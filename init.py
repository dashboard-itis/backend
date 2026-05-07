import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))

from app.bootstrap.rbac import RBACBootstrapper
from app.db.database import AsyncSessionLocal
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository


async def init_rbac() -> None:
    async with AsyncSessionLocal() as session:
        bootstrapper = RBACBootstrapper(
            user_repo=UserRepository(session),
            role_repo=RoleRepository(session),
            permission_repo=PermissionRepository(session),
        )
        await bootstrapper.bootstrap()


if __name__ == '__main__':
    asyncio.run(init_rbac())
