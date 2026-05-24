from app.dependencies.repositories import GradeRepositoryDep
from app.models.grade import GradeCreate, GradePublic, GradeUpdate
from app.schemas.base import PaginatedResponse
from app.schemas.grade import StudentGradeResponse


class GradeService:
    def __init__(self, grade_repo: GradeRepositoryDep):
        self.grade_repo = grade_repo

    def _to_student_grade_response(self, grade) -> StudentGradeResponse:
        assignment = grade.assignment
        course = assignment.course if assignment else None

        return StudentGradeResponse(
            id=grade.id,
            student_id=grade.student_id,
            assignment_id=grade.assignment_id,
            score=grade.score,
            comment=grade.comment,
            created_at=grade.created_at,
            updated_at=grade.updated_at,
            course_name=course.name if course else None,
            assignment_title=assignment.title if assignment else None,
        )

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> PaginatedResponse[StudentGradeResponse]:
        total = await self.grade_repo.count()
        grades = await self.grade_repo.fetch_with_relations(skip=skip, limit=limit)

        return PaginatedResponse[StudentGradeResponse](
            items=[self._to_student_grade_response(grade) for grade in grades],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, grade_id: int) -> StudentGradeResponse | None:
        grade = await self.grade_repo.get_with_relations(grade_id)
        return self._to_student_grade_response(grade) if grade else None

    async def create(self, grade_data: GradeCreate) -> GradePublic:
        await self._validate_references(
            student_id=grade_data.student_id,
            assignment_id=grade_data.assignment_id,
        )
        grade = await self.grade_repo.create(**grade_data.model_dump())
        return GradePublic.model_validate(grade)

    async def update(
        self,
        grade_id: int,
        grade_data: GradeUpdate,
    ) -> GradePublic | None:
        existing = await self.grade_repo.get(grade_id)

        if existing is None:
            return None

        update_data = grade_data.model_dump(exclude_unset=True)
        await self._validate_references(
            student_id=update_data.get('student_id'),
            assignment_id=update_data.get('assignment_id'),
        )

        grade = await self.grade_repo.update(grade_id, **update_data)
        return GradePublic.model_validate(grade) if grade else None

    async def delete(self, grade_id: int) -> bool:
        grade = await self.grade_repo.delete(grade_id)
        return grade is not None

    async def get_student_grades(
        self,
        student_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> PaginatedResponse[StudentGradeResponse]:
        total = await self.grade_repo.count(filters={'student_id': student_id})
        grades = await self.grade_repo.get_student_grades_with_course(
            student_id=student_id,
            skip=skip,
            limit=limit,
        )

        return PaginatedResponse[StudentGradeResponse](
            items=[self._to_student_grade_response(grade) for grade in grades],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def _validate_references(
        self,
        student_id: int | None = None,
        assignment_id: int | None = None,
    ) -> None:
        if student_id is not None and not await self.grade_repo.student_exists(
            student_id
        ):
            raise ValueError('Student not found')

        if assignment_id is not None and not await self.grade_repo.assignment_exists(
            assignment_id
        ):
            raise ValueError('Assignment not found')
