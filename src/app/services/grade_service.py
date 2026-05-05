from app.dependencies.repositories import GradeRepositoryDep
from app.schemas.grade import StudentGradeResponse


class GradeService:
    def __init__(self, grade_repo: GradeRepositoryDep):
        self.grade_repo = grade_repo

    async def get_student_grades(
        self,
        student_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[StudentGradeResponse]:
        grades = await self.grade_repo.get_student_grades_with_course(
            student_id=student_id,
            skip=skip,
            limit=limit,
        )

        result = []

        for grade in grades:
            assignment = grade.assignment
            course = assignment.course if assignment else None

            result.append(
                StudentGradeResponse(
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
            )

        return result
