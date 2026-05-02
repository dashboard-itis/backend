from app.dependencies.session import SessionDep
from app.models.group import Group
from app.repositories.base import Repository


class GroupRepository(Repository[Group]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Group)
