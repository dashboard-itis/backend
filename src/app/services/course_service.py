from app.dependencies.session import SessionDep
from app.utils.repository import Repository
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CoursePublic
from typing import Optional


class CourseService:
    def __init__(self, db: SessionDep):
        self.db = db
        self.repo = Repository[Course](db, Course)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        stream_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> list[CoursePublic]:

        filters = {}
        if name:
            filters["name"] = name
        if stream_id:
            filters["stream_id"] = stream_id
        if teacher_id:
            filters["teacher_id"] = teacher_id

        courses = await self.repo.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            search=search
        )

        return [CoursePublic.model_validate(c) for c in courses]

    async def get_by_id(self, course_id: int) -> Optional[CoursePublic]:
        course = await self.repo.get(course_id)
        return CoursePublic.model_validate(course) if course else None

    async def create(self, course_data: CourseCreate) -> CoursePublic:
        course = await self.repo.create(**course_data.model_dump())
        return CoursePublic.model_validate(course)

    async def update(self, course_id: int, course_data: CourseUpdate) -> Optional[CoursePublic]:
        update_data = course_data.model_dump(exclude_unset=True)

        course = await self.repo.update(course_id, **update_data)
        return CoursePublic.model_validate(course) if course else None

    async def delete(self, course_id: int) -> bool:
        course = await self.repo.delete(course_id)
        return course is not None