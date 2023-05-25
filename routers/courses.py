from fastapi import APIRouter, HTTPException, status, Header, Body
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from data.models import  ViewStudentCourse, Course, CourseUpdate, Section, Report, User
from services import  courses_service, users_service
from data.common.responses import BadRequest, InternalServerError, NoContent, NotFound, Unauthorized
from data.common.auth import get_user_params_or_raise_error, get_user_or_raise_401


course_router = APIRouter(prefix="/courses")

class CourseResponseModel(BaseModel):
    course: Course
    sections: list[Section]

@course_router.get('/enrolled_courses', tags=['Users'], response_model=list[ViewStudentCourse])
def view_enrolled_courses(title: str | None = None,
                          tag: str | None = None, 
                          token: str =Header()) -> list[ViewStudentCourse]:
    ''' View enrolled public and premium courses by students only'''

    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    

    if role == 'student':
        return courses_service.view_enrolled_courses(id, title, tag)
        
    else:
        return JSONResponse(status_code=409,content={'detail': 'Only students can view their enrolled courses!'} )
    

@course_router.get('/', tags=['Users'])
def view_all_courses(title: str | None = None,
                     tag: str | None = None,
                     token: str =Header()):
    ''' View all courses depending on role - anonymous, student, teacher'''
    if not token:
        return courses_service.view_public_courses()
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY Anonymous users!'})
    
    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    
    if role == 'student':
        return courses_service.view_students_courses(title, tag)
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Students'} )
    elif role == 'teacher':
        return courses_service.view_teacher_course(id, title, tag)
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Teachers'})
    # elif role == 'admin':
    #     return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Admin'} )
    
@course_router.put('/{course_id}/ratings', tags=['Users'])
def course_rating(course_id: int, rating: float=Body(embed=True, ge=0, le=10), token: str =Header()):
    ''' Students can rate their enrolled courses only once'''
    token_params=get_user_params_or_raise_error(token)
    
    student_id=token_params[0]
    role=token_params[2]
    

    if role == 'student':
        result=courses_service.course_rating(rating, course_id, student_id)
        if result:
            return JSONResponse(status_code=200,content={'message': 'Student successfully rated this course!'})
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY!Students rate courses'} )
    
    return JSONResponse(status_code=409,content={'detail': 'You are not allowed to rate this course!'} )


@course_router.get('/{course_id}')
def get_course(course_id: int, token: str = Header()):
    get_user_or_raise_401(token)
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound()
    else: 
        return CourseResponseModel(
            course=course, 
            sections=courses_service.get_sections_by_course(course_id))


@course_router.get('/reports')
def get_reports_for_all_owned_courses(token: str = Header()):
    user = get_user_or_raise_401(token)
    result = courses_service.get_all_reports(user.id)

    return result


@course_router.get('/{course_id}/reports')
def get_reports_by_course_id(course_id: int, token: str = Header()):
    user = get_user_or_raise_401(token)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Unauthorized('Only the course owner has access to its reports.')

    result = courses_service.get_reports_by_id(course_id)

    return result


@course_router.post('/', status_code=status.HTTP_201_CREATED)
def create_course(course: Course, token: str = Header()):
    user = get_user_or_raise_401(token)
    if not user.is_teacher():
        return Unauthorized('Only a teacher can create courses.')

    created_course = courses_service.create_course(course)

    return CourseResponseModel(course=created_course, sections=[])


@course_router.put('/{course_id}')
def update_course(course_id: int, data: CourseUpdate, token: str = Header()):
    user = get_user_or_raise_401(token)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Unauthorized('Only the course owner can modify it.')

    updated_course = courses_service.update_course(data, course)
    if updated_course is None:
        return InternalServerError('Failed to update the course.')

    return updated_course


@course_router.post('/{course_id}', status_code=status.HTTP_201_CREATED)
def create_section(course_id: int, section: Section, token: str = Header()):
    user = get_user_or_raise_401(token)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Unauthorized('Only the course owner can create sections within it.')
    
    created_section = courses_service.create_section(course_id, section)
    created_section.courses_id = course_id

    return created_section


@course_router.put('/{course_id}/sections/{section_id}')
def update_section(course_id: int, section_id: int, section: Section, token: str = Header()):
    user = get_user_or_raise_401(token)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound(f'Course {course_id} does not exist!')

    if not user.is_course_owner(course):
        return Unauthorized('Only the course owner can update sections within it.')
    
    existing_section = courses_service.get_section_by_id(section_id)
    if existing_section is None:
        return NotFound()
    else:
        return courses_service.update_section(existing_section, section)


