from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.session import SessionDep
from app.services.course_service import CourseService
from app.schemas.course import CourseCreate, CourseUpdate, CoursePublic
from app.schemas.course_filters import CourseFilters

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CoursePublic])
async def get_courses(
    db: SessionDep,
    filters: CourseFilters = Depends()
):
    service = CourseService(db)
    return await service.get_all(
        skip=filters.skip,
        limit=filters.limit,
        name=filters.name,
        stream_id=filters.stream_id,
        teacher_id=filters.teacher_id,
        search=filters.search
    )

@router.get("/{course_id}", response_model=CoursePublic)
async def get_course(course_id: int, db: SessionDep):
    service = CourseService(db)
    course = await service.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.post("/", response_model=CoursePublic, status_code=status.HTTP_201_CREATED)
async def create_course(course_data: CourseCreate, db: SessionDep):
    service = CourseService(db)
    return await service.create(course_data)

@router.put("/{course_id}", response_model=CoursePublic)
async def update_course(course_id: int, course_data: CourseUpdate, db: SessionDep):
    service = CourseService(db)
    course = await service.update(course_id, course_data)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: SessionDep):
    service = CourseService(db)
    deleted = await service.delete(course_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")