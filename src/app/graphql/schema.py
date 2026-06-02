from typing import Any

import strawberry
from strawberry.types import Info

from app.core.exceptions import NotFoundError
from app.graphql.context import GraphQLContext, require_current_user
from app.graphql.types import (
    CourseCreateInput,
    CourseFilterInput,
    CourseListType,
    CourseType,
    CourseUpdateInput,
    DeleteCourseResult,
)
from app.models.course import CourseCreate, CourseUpdate
from app.schemas.course_filters import CourseFilters


def _context(info: Info) -> GraphQLContext:
    return info.context


def _course_update_data(course_data: CourseUpdateInput) -> dict[str, Any]:
    data: dict[str, Any] = {}

    for field_name in ('name', 'description', 'stream_id', 'teacher_id'):
        value = getattr(course_data, field_name)

        if value is not strawberry.UNSET:
            data[field_name] = value

    return data


@strawberry.type
class Query:
    @strawberry.field
    async def courses(
        self,
        info: Info,
        filters: CourseFilterInput | None = None,
    ) -> CourseListType:
        context = _context(info)
        await require_current_user(context, scopes=['courses:list'])

        filters = filters or CourseFilterInput()
        filters = CourseFilters(
            skip=filters.skip,
            limit=filters.limit,
            search=filters.search,
            name=filters.name,
            stream_id=filters.stream_id,
            teacher_id=filters.teacher_id,
        )
        courses = await context['course_service'].get_all(filters)

        return CourseListType.from_paginated(courses)

    @strawberry.field
    async def course(self, info: Info, course_id: int) -> CourseType:
        context = _context(info)
        await require_current_user(context, scopes=['courses:read'])

        course = await context['course_service'].get_by_id(course_id)

        if course is None:
            raise NotFoundError('Course not found')

        return CourseType.from_public(course)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_course(
        self,
        info: Info,
        course_data: CourseCreateInput,
    ) -> CourseType:
        context = _context(info)
        await require_current_user(context, scopes=['courses:create'])

        course = await context['course_service'].create(
            CourseCreate(
                name=course_data.name,
                description=course_data.description,
                stream_id=course_data.stream_id,
                teacher_id=course_data.teacher_id,
            ),
        )

        return CourseType.from_public(course)

    @strawberry.mutation
    async def update_course(
        self,
        info: Info,
        course_id: int,
        course_data: CourseUpdateInput,
    ) -> CourseType:
        context = _context(info)
        await require_current_user(context, scopes=['courses:update'])

        course = await context['course_service'].update(
            course_id,
            CourseUpdate(**_course_update_data(course_data)),
        )

        if course is None:
            raise NotFoundError('Course not found')

        return CourseType.from_public(course)

    @strawberry.mutation
    async def delete_course(
        self,
        info: Info,
        course_id: int,
    ) -> DeleteCourseResult:
        context = _context(info)
        await require_current_user(context, scopes=['courses:delete'])

        deleted = await context['course_service'].delete(course_id)

        if not deleted:
            raise NotFoundError('Course not found')

        return DeleteCourseResult(deleted=True)


schema = strawberry.Schema(query=Query, mutation=Mutation)
