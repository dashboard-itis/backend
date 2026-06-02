from datetime import datetime

import strawberry

from app.models.course import CoursePublic
from app.schemas.base import PaginatedResponse


@strawberry.type
class CourseType:
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    description: str | None
    stream_id: int | None
    teacher_id: int | None

    @classmethod
    def from_public(cls, course: CoursePublic) -> 'CourseType':
        return cls(
            id=course.id,
            created_at=course.created_at,
            updated_at=course.updated_at,
            name=course.name,
            description=course.description,
            stream_id=course.stream_id,
            teacher_id=course.teacher_id,
        )


@strawberry.type
class CourseListType:
    items: list[CourseType]
    total: int
    skip: int
    limit: int

    @classmethod
    def from_paginated(
        cls,
        courses: PaginatedResponse[CoursePublic],
    ) -> 'CourseListType':
        return cls(
            items=[CourseType.from_public(course) for course in courses.items],
            total=courses.total,
            skip=courses.skip,
            limit=courses.limit,
        )


@strawberry.input
class CourseFilterInput:
    skip: int = 0
    limit: int = 100
    search: str | None = None
    name: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None


@strawberry.input
class CourseCreateInput:
    name: str
    description: str | None = None
    stream_id: int | None = None
    teacher_id: int | None = None


@strawberry.input
class CourseUpdateInput:
    name: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    stream_id: int | None = strawberry.UNSET
    teacher_id: int | None = strawberry.UNSET


@strawberry.type
class DeleteCourseResult:
    deleted: bool
