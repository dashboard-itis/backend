from typing import Literal

from pydantic import BaseModel


TrendPeriod = Literal['week', 'month', 'semester']


class TrendPoint(BaseModel):
    period: str
    average_score: float


class GroupAnalytics(BaseModel):
    group_id: int
    average_score: float
    submission_rate: float
    attendance_rate: float
    distribution: dict[str, int]
    trend: list[TrendPoint]


class StudentAnalytics(BaseModel):
    student_id: int
    average_score: float
    trend: list[TrendPoint]
