# '''Contains the functions related exclusively to administrative actions on courses.'''

# from fastapi import APIRouter, Header
# from data.common.auth import get_user_or_raise_401
# from services import  courses_service
# from data.common.responses import OK200, NotFound404, Conflict409, InternalServerError500
# from data.common.exceptions import Exception403Forbidden
# from courses.course_router import course_router

# @course_router.delete('/{course_id}/student_removals/{student_id}', tags=['Courses'])
# def admin_removes_student_from_course(course_id: int, student_id: int, authorization: str = Header()):
#     ''' Admin removes student from course'''

#     if authorization is None:
#         raise Exception403Forbidden()
    
#     if not courses_service.is_student_enrolled_in_course(course_id,student_id):
#         return Conflict409(f'The student with ID:{student_id} is not enrolled in course with ID:{course_id}.')
    
#     user = get_user_or_raise_401(authorization)
#     if user.is_admin():
#         if courses_service.admin_removes_student_from_course(course_id,student_id):
#             return OK200(f'The student with ID:{student_id} is removed from course with ID:{course_id}.')
#         return Conflict409('Something went wrong.Try again.')

#     return Conflict409('You are not an administator.')

# @course_router.get('/{course_id}/rating_histories', tags=['Courses'])
# def admin_views_students_ratings(course_id: int, authorization: str = Header()):
#     '''Admin only: view students ratings for a course'''
#     if authorization is None:
#         raise Exception403Forbidden()
    
#     course = courses_service.get_course_by_id(course_id)
#     if course is None:
#         return NotFound404(f'Course {course_id} does not exist!')
    
#     user = get_user_or_raise_401(authorization)
#     if user.is_admin():
#         history=courses_service.rating_history(course_id)
#         if history:
#             return history
#         return NotFound404(f'There are no students in course {course_id}')

# @course_router.put('/{course_id}/removals', tags=['Courses'])
# def admin_removes_course(course_id: int, authorization: str = Header()):
#     '''Admin only: removes/hides a course'''
#     if authorization is None:
#         raise Exception403Forbidden()
    
#     course = courses_service.get_course_by_id(course_id)
#     if course is None:
#         return NotFound404(f'Course {course_id} does not exist!')
    
#     if courses_service.is_course_active(course_id):
#         user = get_user_or_raise_401(authorization)
#         if user.is_admin():
#             if courses_service.admin_removes_course(course_id):
#                 return OK200(f'Course {course_id} has been hidden.')
#             return InternalServerError500('Something went wrong. The course has been hidden, but notifications were not sent.')
#     return Conflict409(f'Course {course_id} is already hidden!')