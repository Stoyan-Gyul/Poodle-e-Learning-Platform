'''Contains the functions related to viewing courses.'''

from fastapi import APIRouter, Header
from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin
from data.common.exceptions import Exception403Forbidden
from services import  courses_service
from data.common.models.view_courses import ViewStudentCourse
from data.common.responses import Conflict409


course_router = APIRouter(prefix="/courses")

@course_router.get('/enrolled_courses', tags=['Courses'], response_model=list[ViewStudentCourse])
def view_enrolled_courses(title: str | None = None,
                          tag: str | None = None, 
                          authorization: str =Header(None)) -> list[ViewStudentCourse]:
    ''' View enrolled public and premium courses by students only'''
    if authorization is None:
        raise Exception403Forbidden()

    user = get_user_or_raise_401(authorization)
    id=user.id
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')

    if user.is_student():
        return courses_service.view_enrolled_courses(id, title, tag)

    else:
        return Conflict409('Only students can view their enrolled courses!')


@course_router.get('/', tags=['Courses'])
def view_all_courses(title: str | None = None,
                     rating: float = None,
                     tag: str | None = None,
                     teacher: str = None,
                     student: str  = None,
                     authorization: str =Header(None)):
    ''' View all courses depending on role - anonymous, student, teacher, admin'''
    if not authorization:
        return courses_service.view_public_courses(rating,tag)

    user = get_user_or_raise_401(authorization)
    id=user.id
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    if user.is_student():
        return courses_service.view_students_courses(id, title, tag)

    elif user.is_teacher():
        return courses_service.view_teacher_courses(id, title, tag)
    
    elif user.is_admin():
        return courses_service.view_admin_courses(title, tag, teacher, student)