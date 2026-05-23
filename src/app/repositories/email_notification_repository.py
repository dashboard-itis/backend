from datetime import datetime

from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.email_notification import EmailNotification
from app.repositories.base import Repository


class EmailNotificationRepository(Repository[EmailNotification]):
    def __init__(self, session: SessionDep):
        super().__init__(session, EmailNotification)

    async def get_active(
        self,
        user_id: int,
        action: str,
        code: str,
    ) -> EmailNotification | None:
        result = await self.session.exec(
            select(EmailNotification).where(
                EmailNotification.user_id == user_id,
                EmailNotification.action == action,
                EmailNotification.code == code,
                EmailNotification.is_used.is_(False),
                EmailNotification.expires_at > datetime.utcnow(),
            )
        )
        return result.first()
