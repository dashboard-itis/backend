from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.services import CourseServiceDep
from app.models.course import CourseCreate, CoursePublic, CourseUpdate
from app.schemas.course_filters import CourseFilters

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[CoursePublic])
async def get_courses(
    service: CourseServiceDep,
    filters: CourseFilters = Depends(),
):
    return await service.get_all(filters)


@router.get("/{course_id}", response_model=CoursePublic)
async def get_course(course_id: int, service: CourseServiceDep):
    course = await service.get_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return course


@router.post("/", response_model=CoursePublic, status_code=status.HTTP_201_CREATED)
async def create_course(course_data: CourseCreate, service: CourseServiceDep):
    return await service.create(course_data)


@router.put("/{course_id}", response_model=CoursePublic)
async def update_course(course_id: int, course_data: CourseUpdate, service: CourseServiceDep):
    course = await service.update(course_id, course_data)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, service: CourseServiceDep):
    deleted = await service.delete(course_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )