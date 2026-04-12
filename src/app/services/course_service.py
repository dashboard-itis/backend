from typing import Optional

from app.dependencies.repositories import CourseRepositoryDep
from app.schemas.course import CourseCreate, CoursePublic, CourseUpdate


class CourseService:
    def __init__(self, repo: CourseRepositoryDep):
        self.repo = repo

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        stream_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> list[CoursePublic]:
        filters = {
            "name": name,
            "stream_id": stream_id,
            "teacher_id": teacher_id,
        }
        filters = {key: value for key, value in filters.items() if value is not None}

        courses = await self.repo.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            search=search,
        )
        return [CoursePublic.model_validate(course) for course in courses]

    async def get_by_id(self, course_id: int) -> CoursePublic | None:
        course = await self.repo.get(course_id)
        return CoursePublic.model_validate(course) if course else None

    async def create(self, course_data: CourseCreate) -> CoursePublic:
        course = await self.repo.create(**course_data.model_dump())
        return CoursePublic.model_validate(course)

    async def update(self, course_id: int, course_data: CourseUpdate) -> CoursePublic | None:
        update_data = course_data.model_dump(exclude_unset=True)
        course = await self.repo.update(course_id, **update_data)
        return CoursePublic.model_validate(course) if course else None

    async def delete(self, course_id: int) -> bool:
        deleted = await self.repo.delete(course_id)
        return deleted is not None