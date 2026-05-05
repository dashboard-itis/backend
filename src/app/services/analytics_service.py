from app.dependencies.repositories import (
    AttendanceRepositoryDep,
    GradeRepositoryDep,
    SubmissionRepositoryDep,
)
from app.schemas.analytics import GroupAnalytics


class AnalyticsService:
    def __init__(
        self,
        grade_repo: GradeRepositoryDep,
        attendance_repo: AttendanceRepositoryDep,
        submission_repo: SubmissionRepositoryDep,
    ):
        self.grade_repo = grade_repo
        self.attendance_repo = attendance_repo
        self.submission_repo = submission_repo

    async def get_group_analytics(self, group_id: int) -> GroupAnalytics:
        average_score = await self.grade_repo.get_group_average_score(group_id)
        distribution = await self.grade_repo.get_group_grade_distribution(group_id)
        trend = await self.grade_repo.get_group_trend(group_id)
        attendance_rate = await self.attendance_repo.get_group_attendance_rate(group_id)
        submission_rate = await self.submission_repo.get_group_submission_rate(group_id)

        return GroupAnalytics(
            group_id=group_id,
            average_score=round(average_score, 2),
            submission_rate=submission_rate,
            attendance_rate=attendance_rate,
            distribution=distribution,
            trend=trend,
        )
