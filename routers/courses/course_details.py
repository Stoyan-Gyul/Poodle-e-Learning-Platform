'''Contains the functions related to retrieving course details.'''

from fastapi import APIRouter, Header
from services import courses_service
from data.common.responses import NotFound404, Conflict409, InternalServerError500
from data.common.exceptions import Exception403Forbidden
from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin


course_router = APIRouter(prefix="/courses")

@course_router.get('/{course_id}', tags=['Courses'])
def get_course(course_id: int, authorization: str = Header()):
    '''Retrieve course details.'''

    get_user_or_raise_401(authorization)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')

    tags = courses_service.get_course_tags(course.id)
    objectives = courses_service.get_course_objectives(course.id)
    sections = courses_service.get_course_sections(course.id)

    return courses_service.create_response_object(course, tags, objectives, sections)


@course_router.get('/{course_id}/sections/{section_id}', tags=['Courses'])
def view_section(course_id: int,section_id: int, authorization: str = Header()):
    ''' View a section of a course'''

    if authorization is None:
        raise Exception403Forbidden() 

    user = get_user_or_raise_401(authorization)
    user_id=user.id
    # Verify if role is approved
    if not is_user_approved_by_admin(user_id):
        return Conflict409('Your role is still not approved.')
    #verify if user enrolled in course
    if not courses_service.is_student_enrolled_in_course(course_id, user_id):
        return NotFound404('This student is not enrolled in this course.')
    # verify if course has section
    if not courses_service.has_course_section(course_id, section_id):
        return NotFound404('This course has not this section')
    section=courses_service.view_section(course_id, section_id, user_id)
    if section is None:
        return InternalServerError500('Something went wrong. Try again.')
    
    return section



