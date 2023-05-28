from fastapi import APIRouter, status, Header, Body
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from data.models import  ViewStudentCourse, Course, CourseUpdate, Section
from services import  courses_service
from data.common.responses import InternalServerError, NotFound, Forbidden
from data.common.auth import get_user_or_raise_401


course_router = APIRouter(prefix="/courses")

class CourseResponseModel(BaseModel):
    course: Course
    sections: list[Section]

@course_router.get('/enrolled_courses', tags=['Courses'], response_model=list[ViewStudentCourse])
def view_enrolled_courses(title: str | None = None,
                          tag: str | None = None, 
                          authorization: str =Header()) -> list[ViewStudentCourse]:
    ''' View enrolled public and premium courses by students only'''

    # token_params=get_user_params_or_raise_error(token)
    
    # id=token_params[0]
    # role=token_params[2]
    user = get_user_or_raise_401(authorization)
    id=user.id

    # if role == 'student':
    if user.is_student():
        return courses_service.view_enrolled_courses(id, title, tag)
        
    else:
        return JSONResponse(status_code=409,content={'detail': 'Only students can view their enrolled courses!'} )
    

@course_router.get('/', tags=['Courses'])
def view_all_courses(title: str | None = None,
                     rating: float = None,
                     tag: str | None = None,
                     authorization: str =Header()):
    ''' View all courses depending on role - anonymous, student, teacher'''
    if not authorization:
        return courses_service.view_public_courses(rating,tag)
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY Anonymous users!'})
    
    # token_params=get_user_params_or_raise_error(token)
    
    # id=token_params[0]
    # role=token_params[2]

    user = get_user_or_raise_401(authorization)
    id=user.id
    
    # if role == 'student':
    if user.is_student():
        return courses_service.view_students_courses(title, tag)
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Students'} )
    # elif role == 'teacher':
    elif user.is_teacher() or user.is_admin():
        return courses_service.view_teacher_courses(id, title, tag)
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Teachers'})
    # elif role == 'admin':
    #     return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Admin'} )
    
@course_router.put('/{course_id}/ratings', tags=['Courses'])
def course_rating(course_id: int, rating: int=Body(embed=True, ge=0, le=10), authorization: str =Header()):
    ''' Students can rate their enrolled courses only once'''
    # token_params=get_user_params_or_raise_error(token)
    
    # student_id=token_params[0]
    # role=token_params[2]
    user = get_user_or_raise_401(authorization)
    student_id=user.id

    # if role == 'student':
    if user.is_student():
        result=courses_service.course_rating(rating, course_id, student_id)
        if result:
            return JSONResponse(status_code=200,content={'message': 'Student successfully rated this course!'})
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY!Students rate courses'} )
    
    return JSONResponse(status_code=409,content={'detail': 'You are not allowed to rate this course!'} )


@course_router.get('/reports', tags=['Courses'])
def get_reports_for_all_owned_courses(authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    result = courses_service.get_all_reports(user.id)

    return result

@course_router.get('/{course_id}', tags=['Courses'])
def get_course(course_id: int, authorization: str = Header()):
    get_user_or_raise_401(authorization)
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')
    else: 
        return CourseResponseModel(
            course=course, 
            sections=courses_service.get_sections_by_course(course_id))

@course_router.get('/{course_id}/reports', tags=['Courses'])
def get_reports_by_course_id(course_id: int, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden('Only the course owner has access to its reports.')

    result = courses_service.get_reports_by_id(course_id)

    return result


@course_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_course(course: Course, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    if not user.is_teacher():
        return Forbidden('Only a teacher can create courses.')

    created_course = courses_service.create_course(course)

    return CourseResponseModel(course=created_course, sections=[])


@course_router.put('/{course_id}', tags=['Courses'])
def update_course(course_id: int, data: CourseUpdate, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden('Only the course owner can modify the course.')

    updated_course = courses_service.update_course(data, course)
    if updated_course is None:
        return InternalServerError('Failed to update the course.')

    return updated_course


@course_router.post('/{course_id}', status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_section(course_id: int, section: Section, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden('Only the course owner can create sections within it.')

    created_section = courses_service.create_section(course_id, section)
    created_section.courses_id = course_id

    return created_section


@course_router.put('/{course_id}/sections/{section_id}',tags=['Courses'])
def update_section(course_id: int, section_id: int, section: Section, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Forbidden('Only the course owner can update sections within it.')

    existing_section = courses_service.get_section_by_id(section_id)
    if existing_section is None:
        return NotFound(f'Section {section_id} does not exist!')
    else:
        return courses_service.update_section(existing_section, section)


