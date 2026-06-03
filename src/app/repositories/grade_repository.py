from typing import Literal

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.models.course import Course
from app.models.grade import Grade
from app.models.group import Group
from app.models.stream import Stream
from app.models.user import User
from app.repositories.base import Repository

TrendPeriod = Literal['week', 'month', 'semester']

GRADE_A_MIN_SCORE = 90
GRADE_B_MIN_SCORE = 75
GRADE_C_MIN_SCORE = 60
GRADE_D_MIN_SCORE = 50


class GradeRepository(Repository[Grade]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Grade)

    async def get_with_relations(self, grade_id: int) -> Grade | None:
        result = await self.session.exec(
            select(Grade)
            .where(Grade.id == grade_id)
            .options(selectinload(Grade.course))
        )
        return result.first()

    async def fetch_with_relations(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Grade]:
        result = await self.session.exec(
            select(Grade)
            .options(selectinload(Grade.course))
            .offset(skip)
            .limit(limit)
        )
        return list(result.all())

    async def fetch_export_rows(
        self,
        student_id: int | None = None,
        course_id: int | None = None,
        group_id: int | None = None,
    ) -> list[tuple[str, str, str, int | None, str | None, str, float, str | None]]:
        query = (
            select(
                User.email,
                User.last_name,
                User.first_name,
                User.group_id,
                Group.name,
                Course.name,
                Grade.score,
                Grade.comment,
            )
            .join(User, Grade.student_id == User.id)
            .join(Course, Grade.course_id == Course.id)
            .outerjoin(Group, User.group_id == Group.id)
            .order_by(User.last_name, User.first_name, Course.name, Grade.created_at)
        )

        if student_id is not None:
            query = query.where(Grade.student_id == student_id)

        if course_id is not None:
            query = query.where(Grade.course_id == course_id)

        if group_id is not None:
            query = query.where(User.group_id == group_id)

        result = await self.session.exec(query)
        return list(result.all())

    async def student_exists(self, student_id: int) -> bool:
        result = await self.session.exec(select(User.id).where(User.id == student_id))
        return result.first() is not None

    async def course_exists(self, course_id: int) -> bool:
        result = await self.session.exec(
            select(Course.id).where(Course.id == course_id)
        )
        return result.first() is not None

    async def get_student_id_by_email(self, email: str) -> int | None:
        result = await self.session.exec(
            select(User.id).where(func.lower(User.email) == email.lower())
        )
        return result.first()

    async def get_course_id_by_name(self, name: str) -> int | None:
        result = await self.session.exec(
            select(Course.id).where(func.lower(Course.name) == name.lower())
        )
        return result.first()

    async def get_student_grades_with_course(
        self,
        student_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Grade]:
        result = await self.session.exec(
            select(Grade)
            .where(Grade.student_id == student_id)
            .options(selectinload(Grade.course))
            .offset(skip)
            .limit(limit)
        )
        return list(result.all())

    async def get_group_average_score(self, group_id: int) -> float:
        result = await self.session.exec(
            select(func.avg(Grade.score))
            .join(Course, Grade.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
        )

        average = result.one_or_none()
        return float(average or 0)

    async def get_group_grade_distribution(self, group_id: int) -> dict[str, int]:
        result = await self.session.exec(
            select(Grade.score)
            .join(Course, Grade.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
        )

        scores = list(result.all())

        distribution = {
            'A': 0,
            'B': 0,
            'C': 0,
            'D': 0,
            'F': 0,
        }

        for score in scores:
            if score >= GRADE_A_MIN_SCORE:
                distribution['A'] += 1
            elif score >= GRADE_B_MIN_SCORE:
                distribution['B'] += 1
            elif score >= GRADE_C_MIN_SCORE:
                distribution['C'] += 1
            elif score >= GRADE_D_MIN_SCORE:
                distribution['D'] += 1
            else:
                distribution['F'] += 1

        return distribution

    def _date_trunc_period(self, trend_period: TrendPeriod):
        if trend_period == 'month':
            return func.date_trunc('month', Grade.created_at)

        return func.date_trunc('week', Grade.created_at)

    def _format_trend_period(self, period, trend_period: TrendPeriod) -> str:
        if trend_period == 'month':
            return period.strftime('%Y-%m')

        return f'{period.isocalendar().year}-W{period.isocalendar().week:02d}'

    async def get_group_trend(
        self,
        group_id: int,
        trend_period: TrendPeriod = 'semester',
    ) -> list[dict]:
        if trend_period == 'semester':
            result = await self.session.exec(
                select(
                    Stream.semester,
                    Stream.year,
                    func.avg(Grade.score),
                )
                .join(Course, Course.stream_id == Stream.id)
                .join(Grade, Grade.course_id == Course.id)
                .where(Stream.group_id == group_id)
                .group_by(Stream.year, Stream.semester)
                .order_by(Stream.year, Stream.semester)
            )

            return [
                {
                    'period': f'{semester} семестр {year}',
                    'average_score': round(float(average_score or 0), 2),
                }
                for semester, year, average_score in result.all()
            ]

        period = self._date_trunc_period(trend_period)
        result = await self.session.exec(
            select(
                period.label('period'),
                func.avg(Grade.score),
            )
            .join(Course, Grade.course_id == Course.id)
            .join(Stream, Course.stream_id == Stream.id)
            .where(Stream.group_id == group_id)
            .group_by(period)
            .order_by(period)
        )

        return [
            {
                'period': self._format_trend_period(period_value, trend_period),
                'average_score': round(float(average_score or 0), 2),
            }
            for period_value, average_score in result.all()
        ]

    async def get_student_average_score(self, student_id: int) -> float:
        result = await self.session.exec(
            select(func.avg(Grade.score)).where(Grade.student_id == student_id)
        )

        average = result.one_or_none()
        return float(average or 0)

    async def get_student_trend(
        self,
        student_id: int,
        trend_period: TrendPeriod = 'semester',
    ) -> list[dict]:
        if trend_period == 'semester':
            result = await self.session.exec(
                select(
                    Stream.semester,
                    Stream.year,
                    func.avg(Grade.score),
                )
                .join(Course, Grade.course_id == Course.id)
                .join(Stream, Course.stream_id == Stream.id)
                .where(Grade.student_id == student_id)
                .group_by(Stream.year, Stream.semester)
                .order_by(Stream.year, Stream.semester)
            )

            return [
                {
                    'period': f'{semester} семестр {year}',
                    'average_score': round(float(average_score or 0), 2),
                }
                for semester, year, average_score in result.all()
            ]

        period = self._date_trunc_period(trend_period)
        result = await self.session.exec(
            select(
                period.label('period'),
                func.avg(Grade.score),
            )
            .where(Grade.student_id == student_id)
            .group_by(period)
            .order_by(period)
        )

        return [
            {
                'period': self._format_trend_period(period_value, trend_period),
                'average_score': round(float(average_score or 0), 2),
            }
            for period_value, average_score in result.all()
        ]
