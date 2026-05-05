from sqlalchemy import func
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.assignment import Assignment
from app.models.course import Course
from app.models.stream import Stream
from app.models.submission import Submission
from app.repositories.base import Repository


class SubmissionRepository(Repository[Submission]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Submission)

    async def get_group_submission_rate(self, group_id: int) -> float:
        total_result = await self.session.exec(
            select(func.count(Submission.id))
            .join(Assignment, Submission.assignment_id == Assignment.id)
            .join(Course, Assignment.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
        )
        total = total_result.one()

        if total == 0:
            return 0

        submitted_result = await self.session.exec(
            select(func.count(Submission.id))
            .join(Assignment, Submission.assignment_id == Assignment.id)
            .join(Course, Assignment.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
        )
        submitted = submitted_result.one()

        return round(submitted / total, 2)
