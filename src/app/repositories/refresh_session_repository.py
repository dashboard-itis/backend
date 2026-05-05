from app.dependencies.session import SessionDep
from app.models.refresh_session import RefreshSession
from app.repositories.base import Repository


class RefreshSessionRepository(Repository[RefreshSession]):
    def __init__(self, session: SessionDep):
        super().__init__(session, RefreshSession)
