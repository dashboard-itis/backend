from app.dependencies.session import SessionDep
from app.models.permission import Permission
from app.repositories.base import Repository


class PermissionRepository(Repository[Permission]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Permission)

    async def get_by_subject_and_action(
        self,
        subject: str,
        action: str,
    ) -> Permission | None:
        permissions = await self.fetch(
            filters={
                'subject': subject,
                'action': action,
            },
            limit=1,
        )
        return permissions[0] if permissions else None

    async def get_or_create(
        self,
        subject: str,
        action: str,
        description: str | None = None,
    ) -> Permission:
        permission = await self.get_by_subject_and_action(subject, action)

        if permission is None:
            permission = await self.create(
                subject=subject,
                action=action,
                description=description,
            )

        return permission
