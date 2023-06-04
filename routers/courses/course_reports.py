'''Contains the functions related to course reports with the exception of sections.'''

from fastapi import APIRouter, Header
from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin
from services import  courses_service
from data.common.responses import Forbidden403, NotFound404, Conflict409


course_router = APIRouter(prefix="/courses")

@course_router.get('/reports', tags=['Courses'])
def get_reports_for_all_owned_courses(authorization: str = Header()):
    '''Get reports for all owned courses.'''

    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    result = courses_service.get_all_reports(user.id)

    return result


@course_router.get('/{course_id}/reports', tags=['Courses'])
def get_reports_by_course_id(course_id: int, authorization: str = Header()):
    '''Get reports for a specific course.'''

    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound404(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden403('Only the course owner has access to its reports.')

    result = courses_service.get_reports_by_id(course_id)

    return result