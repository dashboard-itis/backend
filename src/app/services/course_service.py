from app.dependencies.repositories import CourseRepositoryDep
from app.models.course import CourseCreate, CoursePublic, CourseUpdate
from app.schemas.course_filters import CourseFilters


class CourseService:
    def __init__(self, repo: CourseRepositoryDep):
        self.repo = repo

    async def get_all(self, filters: CourseFilters) -> list[CoursePublic]:
        filters_data = filters.model_dump(
            exclude_none=True,
            exclude={"skip", "limit", "search"},
        )

        courses = await self.repo.get_all(
            skip=filters.skip,
            limit=filters.limit,
            filters=filters_data,
            search=filters.search,
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