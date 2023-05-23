from fastapi import APIRouter, Header, Body
from fastapi.responses import JSONResponse
from data.models import  ViewStudentCourse
from services import  courses_service

from data.common.auth import get_user_params_or_raise_error


course_router = APIRouter(prefix="/courses")

@course_router.get('/enrolled_courses', tags=['Users'], response_model=list[ViewStudentCourse])
def view_enrolled_courses(title: str | None = None,
                          tag: str | None = None, 
                          token: str =Header()) -> list[ViewStudentCourse]:
    ''' View public and enrolled courses by students only'''

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

