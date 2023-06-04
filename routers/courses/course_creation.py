'''Contains the functions related to creating and updating courses.'''

from fastapi import APIRouter, status, Header, UploadFile
from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin
from services import  courses_service
from data.common.responses import OK200, BadRequest400, Forbidden403, NotFound404, Conflict409, InternalServerError500
from data.common.exceptions import Exception403Forbidden
from data.common.models.course import Course
from data.common.models.course_update import CourseUpdate


course_router = APIRouter(prefix="/courses")

@course_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_course(course: Course, authorization: str = Header(None)) -> Course:
    '''Creates a new course.'''

    user = get_user_or_raise_401(authorization)
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    if not user.is_teacher():
        return Forbidden403('Only a teacher can create courses.')

    if course.tag_ids == []:
        return BadRequest400('Must contain at least one tag')
    if course.objective_ids == []:
        return BadRequest400('Must contain at least one objective')

    tags = courses_service.get_tags(course.tag_ids)
    if len(tags) < len(course.tag_ids):
        return BadRequest400('Must contain existing tags')
    objectives = courses_service.get_objectives(course.objective_ids)
    if len(objectives) < len(course.objective_ids):
        return BadRequest400('Must contain existing objectives')

    created_course = courses_service.create_course(course, user)

    return created_course


@course_router.put('/{course_id}', tags=['Courses'])
def update_course(course_id: int, data: CourseUpdate, authorization: str = Header()) -> Course:
    '''Updates an existing course.'''

    user = get_user_or_raise_401(authorization)
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden403('Only the course owner can modify the course.')

    updated_course = courses_service.update_course(data, course)
    if updated_course is None:
        return InternalServerError500('Failed to update the course.')

    return updated_course


@course_router.post('/', tags=['Courses'])
def deactivate_course(course_id: int, authorization: str = Header(None)) -> None:
    '''Deactivates a course.'''

    user = get_user_or_raise_401(authorization)
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden403('Only the course owner can deactivate the course.')


@course_router.put('/pic/{course_id}', tags=['Courses'])
def upload_pic_to_course(course_id: int, pic: UploadFile, authorization: str = Header(None),) -> OK200:
    '''Uploads a picture to a course.'''

    if authorization is None:
        raise Exception403Forbidden()
        
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')
    
    picture_data = pic.file.read()
    courses_service.upload_pic(course_id, picture_data)
    return OK200("Picture uploaded successfully")


