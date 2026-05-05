from app.dependencies.repositories import CourseRepositoryDep
from app.models.course import CourseCreate, CoursePublic, CourseUpdate
from app.schemas.course_filters import CourseFilters


class CourseService:
    def __init__(self, course_repo: CourseRepositoryDep):
        self.course_repo = course_repo

    async def get_all(self, filters: CourseFilters) -> list[CoursePublic]:
        filters_data = filters.model_dump(
            exclude_none=True,
            exclude={'skip', 'limit', 'search'},
        )

        courses = await self.course_repo.fetch(
            skip=filters.skip,
            limit=filters.limit,
            filters=filters_data,
            search=filters.search,
        )
        return [CoursePublic.model_validate(course) for course in courses]

    async def get_by_id(self, course_id: int) -> CoursePublic | None:
        course = await self.course_repo.get(course_id)
        return CoursePublic.model_validate(course) if course else None

    async def create(self, course_data: CourseCreate) -> CoursePublic:
        course = await self.course_repo.create(**course_data.model_dump())
        return CoursePublic.model_validate(course)

    async def update(
        self,
        course_id: int,
        course_data: CourseUpdate,
    ) -> CoursePublic | None:
        update_data = course_data.model_dump(exclude_unset=True)
        course = await self.course_repo.update(course_id, **update_data)
        return CoursePublic.model_validate(course) if course else None

    async def delete(self, course_id: int) -> bool:
        course = await self.course_repo.delete(course_id)
        return course is not None
