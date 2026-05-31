from app.dependencies.session import SessionDep
from app.models.links import UserRoleLink
from app.repositories.base import Repository


class UserRoleLinkRepository(Repository[UserRoleLink]):
    def __init__(self, session: SessionDep):
        super().__init__(session, UserRoleLink)
