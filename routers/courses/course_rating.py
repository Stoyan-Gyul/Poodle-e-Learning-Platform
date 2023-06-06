# '''Contains the functions related to course ratings.'''

# from fastapi import APIRouter, Header, Body
# from data.common.auth import get_user_or_raise_401, is_user_approved_by_admin
# from data.common.exceptions import Exception403Forbidden
# from services import  courses_service
# from data.common.responses import OK200, Conflict409
# from courses.course_router import course_router

# @course_router.put('/{course_id}/ratings', tags=['Courses'])
# def course_rating(course_id: int, rating: int=Body(embed=True, ge=0, le=10), authorization: str=Header(None)):
#     ''' Students can rate their enrolled courses only once'''
#     if authorization is None:
#         raise Exception403Forbidden()
#     user = get_user_or_raise_401(authorization)
#     student_id=user.id
#     # Verify if role is approved
#     if not is_user_approved_by_admin(user.id):
#         return Conflict409('Your role is still not approved.')

#     if user.is_student():
#         result=courses_service.course_rating(rating, course_id, student_id)
#         if result:
#             return OK200('Student successfully rated this course!')
    
#     return Conflict409('You are not allowed to rate this course!')