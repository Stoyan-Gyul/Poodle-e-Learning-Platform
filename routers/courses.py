from fastapi import APIRouter, HTTPException, status, Header, Body, UploadFile
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from data.models import  ViewStudentCourse, Course, CourseResponseModel, CourseUpdate, Section
from services import  courses_service
from data.common.responses import InternalServerError, NotFound, Forbidden, BadRequest, Conflict
from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin


course_router = APIRouter(prefix="/courses")

@course_router.get('/enrolled_courses', tags=['Courses'], response_model=list[ViewStudentCourse])
def view_enrolled_courses(title: str | None = None,
                          tag: str | None = None, 
                          authorization: str =Header(None)) -> list[ViewStudentCourse]:
    ''' View enrolled public and premium courses by students only'''
    if authorization is None:
        raise HTTPException(status_code=403)

    user = get_user_or_raise_401(authorization)
    id=user.id
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})

    if user.is_student():
        return courses_service.view_enrolled_courses(id, title, tag)

    else:
        return JSONResponse(status_code=409,content={'detail': 'Only students can view their enrolled courses!'} )


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
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})
    
    if user.is_student():
        return courses_service.view_students_courses(id, title, tag)

    elif user.is_teacher():
        return courses_service.view_teacher_courses(id, title, tag)
    
    elif user.is_admin():
        return courses_service.view_admin_courses(title, tag, teacher, student)
    

@course_router.put('/{course_id}/ratings', tags=['Courses'])
def course_rating(course_id: int, rating: int=Body(embed=True, ge=0, le=10), authorization: str =Header(None)):
    ''' Students can rate their enrolled courses only once'''
    if authorization is None:
        raise HTTPException(status_code=403)
    user = get_user_or_raise_401(authorization)
    student_id=user.id
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})

    if user.is_student():
        result=courses_service.course_rating(rating, course_id, student_id)
        if result:
            return JSONResponse(status_code=200,content={'message': 'Student successfully rated this course!'})
    
    return JSONResponse(status_code=409,content={'detail': 'You are not allowed to rate this course!'} )


@course_router.get('/reports', tags=['Courses'])
def get_reports_for_all_owned_courses(authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})
    result = courses_service.get_all_reports(user.id)

    return result


@course_router.get('/{course_id}', tags=['Courses'])
def get_course(course_id: int, authorization: str = Header()):

    get_user_or_raise_401(authorization)

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound({'detail': f'Course {course_id} does not exist!'})
    else: 
        return CourseResponseModel(
            course=course, 
            sections=courses_service.get_sections_by_course(course_id))


@course_router.get('/{course_id}/reports', tags=['Courses'])
def get_reports_by_course_id(course_id: int, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound({'detail': f'Course {course_id} does not exist!'})

    if not user.is_course_owner(course):
        return Forbidden({'detail': 'Only the course owner has access to its reports.'})

    result = courses_service.get_reports_by_id(course_id)

    return result


@course_router.post('/', status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_course(course: Course, authorization: str = Header(None)):
    user = get_user_or_raise_401(authorization)
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})
    if not user.is_teacher():
        return Forbidden({'detail': 'Only a teacher can create courses.'})

    if course.tag_ids == []:
        return BadRequest({'detail': 'Must contain at least one tag'})
    if course.objective_ids == []:
        return BadRequest({'detail': 'Must contain at least one objective'})

    tags = courses_service.get_tags(course.tag_ids)
    if len(tags) < len(course.tag_ids):
        return BadRequest({'detail': 'Must contain existing tags'})
    objectives = courses_service.get_objectives(course.objective_ids)
    if len(objectives) < len(course.objective_ids):
        return BadRequest({'detail': 'Must contain existing objectives'})

    created_course = courses_service.create_course(course, user)

    return created_course


@course_router.put('/{course_id}', tags=['Courses'])
def update_course(course_id: int, data: CourseUpdate, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})
    
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound({'detail': f'Course {course_id} does not exist!'})

    if not user.is_course_owner(course):
        return Forbidden({'detail': 'Only the course owner can modify the course.'})

    updated_course = courses_service.update_course(data, course)
    if updated_course is None:
        return InternalServerError({'detail': 'Failed to update the course.'})

    return updated_course


@course_router.post('/', tags=['Courses'])
def deactivate_course(course_id: int, authorization: str = Header(None)):
    user = get_user_or_raise_401(authorization)
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})

    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound({'detail': f'Course {course_id} does not exist!'})

    if not user.is_course_owner(course):
        return Forbidden({'detail': 'Only the course owner can deactivate the course.'})


@course_router.put('/pic/{course_id}', tags=['Courses'])
def upload_pic_to_course(course_id: int, pic: UploadFile, authorization: str = Header(None),):
    
    if authorization is None:
            raise HTTPException(status_code=403)
        
    course = courses_service.get_course_by_id(course_id)
    if course is None:
            return NotFound({'detail': f'Course {course_id} does not exist!'})
    
    picture_data = pic.file.read()
    courses_service.upload_pic(course_id, picture_data)
    return JSONResponse(status_code=200, content={"detail": "Picture uploaded successfully"}) 


@course_router.post('/{course_id}', status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_section(course_id: int, section: Section, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})
    
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound({'detail': f'Course {course_id} does not exist!'})

    if not user.is_course_owner(course):
        return Forbidden({'detail': 'Only the course owner can create sections within it.'})

    created_section = courses_service.create_section(course_id, section)
    created_section.courses_id = course_id

    return created_section


@course_router.put('/{course_id}/sections/{section_id}',tags=['Courses'])
def update_section(course_id: int, section_id: int, section: Section, authorization: str = Header()):
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict({'detail': 'Your role is still not approved.'})
    
    course = courses_service.get_course_by_id(course_id)
    if course is None:
        return NotFound({'detail': f'Course {course_id} does not exist!'})

    if not user.is_course_owner(course):
        return Forbidden({'detail': 'Only the course owner can update sections within it.'})

    existing_section = courses_service.get_section_by_id(section_id)
    if existing_section is None:
        return NotFound({'detail': f'Section {section_id} does not exist!'})
    else:
        return courses_service.update_section(existing_section, section)


@course_router.get('/{course_id}/sections/{section_id}', tags=['Courses'])
def view_section(course_id: int,section_id: int, authorization: str = Header()):
    ''' View section of a course'''

    if authorization is None:
        raise HTTPException(status_code=403) 

    user = get_user_or_raise_401(authorization)
    user_id=user.id
    # Verify if role is approved
    if not is_user_approved_by_admin(user_id):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})
    #verify if user enrolled in course
    if not courses_service.is_student_enrolled_in_course(course_id, user_id):
        return JSONResponse(status_code=404, content={'detail': 'This student is not enrolled in this course.'})
    # verify if course has section
    if not courses_service.has_course_section(course_id, section_id):
        return JSONResponse(status_code=404, content={'detail': 'This course has not this section'})
    section=courses_service.view_section(course_id, section_id, user_id)
    if section is None:
        return JSONResponse(status_code=500, content={'detail': 'Something went wrong. Try again.'})
    
    return section


@course_router.delete('/{course_id}/student_removals/{student_id}', tags=['Courses'])
def admin_removes_student_from_course(course_id: int, student_id: int, authorization: str = Header()):
    ''' Admin removes student from course'''

    if authorization is None:
        raise HTTPException(status_code=403)
    
    if not courses_service.is_student_enrolled_in_course(course_id,student_id):
        return JSONResponse(status_code=409, content={'detail': f'The student with ID:{student_id} is not enrolled in course with ID:{course_id}.'})
    
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        if courses_service.admin_removes_student_from_course(course_id,student_id):
            return JSONResponse(status_code=200, content={'message': f'The student with ID:{student_id} is removed from course with ID:{course_id}.'})
        return JSONResponse(status_code=409, content={'detail': 'Something went wrong.Try again.'})

    return JSONResponse(status_code=409, content={'detail': 'You are not administator.'})

@course_router.get('/{course_id}/rating_histories', tags=['Courses'])
def admin_views_students_ratings(course_id: int, authorization: str = Header()):
        '''Admin only view students ratings for a course'''
        if authorization is None:
            raise HTTPException(status_code=403)
        
        course = courses_service.get_course_by_id(course_id)
        if course is None:
            return NotFound({'detail': f'Course {course_id} does not exist!'})
        
        user = get_user_or_raise_401(authorization)
        if user.is_admin():
            history=courses_service.rating_history(course_id)
            if history:
                return history
            return NotFound({'detail': f'There is no students in course {course_id}'})
        
@course_router.put('/{course_id}/removals', tags=['Courses'])
def admin_removes_course(course_id: int, authorization: str = Header()):
        '''Admin only removes/hide  a course'''
        if authorization is None:
            raise HTTPException(status_code=403)
        
        course = courses_service.get_course_by_id(course_id)
        if course is None:
            return NotFound({'detail': f'Course {course_id} does not exist!'})
        
        if courses_service.is_course_active(course_id):
            user = get_user_or_raise_401(authorization)
            if user.is_admin():
                if courses_service.admin_removes_course(course_id):
                    return JSONResponse(status_code=200, content={'message':f'Course {course_id} has been hidden.'})
                return JSONResponse(status_code=500, content={'detail':'Something went wrong. The course has been hiden but notifications were not sent.'})
        return Conflict({'detail': f'Course {course_id} is already hidden!'})
