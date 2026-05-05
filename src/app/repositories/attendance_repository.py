from sqlalchemy import func
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.attendance import Attendance, AttendanceStatus
from app.models.course import Course
from app.models.stream import Stream
from app.repositories.base import Repository


class AttendanceRepository(Repository[Attendance]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Attendance)

    async def get_group_attendance_rate(self, group_id: int) -> float:
        total_result = await self.session.exec(
            select(func.count(Attendance.id))
            .join(Course, Attendance.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
        )
        total = total_result.one()

        if total == 0:
            return 0

        present_result = await self.session.exec(
            select(func.count(Attendance.id))
            .join(Course, Attendance.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
            .where(Attendance.status == AttendanceStatus.PRESENT)
        )
        present = present_result.one()

        return round(present / total, 2)
