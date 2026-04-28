from app.dependencies.session import SessionDep
from app.models.course import Course
from app.repositories.base import Repository


class CourseRepository(Repository[Course]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Course)
