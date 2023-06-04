'''Contains the functions related to creating and updating sections.'''

from fastapi import APIRouter, status, Header
from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin
from services import  courses_service
from data.common.responses import Forbidden403, NotFound404, Conflict409
from data.common.models.section import Section

course_router = APIRouter(prefix="/courses")


@course_router.post('/{course_id}', status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_section(course_id: int, section: Section, authorization: str = Header()):
    '''Create a section within a course.'''

    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden403('Only the course owner can create sections within it.')

    created_section = courses_service.create_section(course_id, section)
    created_section.courses_id = course_id

    return created_section


@course_router.put('/{course_id}/sections/{section_id}',tags=['Courses'])
def update_section(course_id: int, section_id: int, section: Section, authorization: str = Header()):
    '''Update a section within a course.'''
    
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden403('Only the course owner can update sections within it.')

    existing_section = courses_service.get_section_by_id(section_id)
    if existing_section is None:
        return NotFound404(f'Section {section_id} does not exist!')
    else:
        return courses_service.update_section(existing_section, section)