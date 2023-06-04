from fastapi import APIRouter, Header, status
from data.common.responses import InternalServerError500, NotFound404, Forbidden403, BadRequest400, Conflict409, OK200, Created201
from data.common.exceptions import Exception400BadRequest, Exception403Forbidden, Exception404NotFound, Exception500InternalServerError
from data.common.models.login_data import LoginData
from data.common.models.update_data import UpdateData
from data.common.models.user import User
from services import users_service, courses_service
# from services.users_service import Teacher
from data.common.auth import  get_user_or_raise_401, is_user_approved_by_admin
import uuid

user_router = APIRouter(prefix="/users")


@user_router.post("/", status_code=status.HTTP_201_CREATED, tags=['Users'])
def register_user(user: User):

    if not user.email or not user.password:
        raise Exception400BadRequest("Username or password cannot be empty!")
    
    existing_user = users_service.find_by_email(user.email)
    if existing_user:
        raise Exception400BadRequest("User with this email already exists!")
    
    if user.role is None:
        user.role = 'student'

    try:

        verification_token = str(uuid.uuid4())
        user.verification_token = verification_token

        verification_link =f"http://localhost:8000/users/{user.email}/verification/{verification_token}"

        users_service.create_new_user(user)
        
        users_service.send_verification_email(user.email, verification_link)

        return Created201('You registered successfully. Check your email for verification.')
    except Exception:
        raise Exception500InternalServerError("Something went wrong!")
    
@user_router.get("/{email}/verification/{token}", tags=['Users'])
def verify_email(email:str, token: str):

    if users_service.verify_email(email, token):
        return OK200('User verified successfully.')
    else:
        raise Exception500InternalServerError("Invalid verification token.")
    
@user_router.post('/login', tags=['Users'])
def login(data: LoginData):

    if data.email is None or data.password is None:
        raise Exception400BadRequest("Email or password cannot be empty!")
    
    user = users_service.find_by_email(data.email)

    if user is None:
        raise Exception404NotFound("User with this email does not exist!") 


    if users_service.try_login(user, data.password):
        token = users_service.generate_token(user)
        return OK200(content={'token': token})
    else:
        return BadRequest400('Invalid login data')


@user_router.put('/{user_id}/courses/{course_id}/subscribe', tags=['Users'])
def subscribe_to_course(user_id: int, course_id: int, authorization: str = Header(None)):
    '''Student subscribes to course'''
    if authorization is None:
        raise Exception403Forbidden()
    
    if courses_service.is_student_enrolled_in_course(course_id, user_id): #check if student enrolled in course
        return Conflict409('This student is ALREADY enrolled in this course.')

    user = get_user_or_raise_401(authorization)

    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')

    if not courses_service.course_exists(course_id): 
        return NotFound404(f'Course {course_id} does not exist')

    if user is None:
        raise Exception404NotFound(f"User {user_id} does not exist")
    
    if not user.id == user_id:
        raise Exception403Forbidden()
    
    # prevent user to subscribe to more than 5 premium courses
    if courses_service.is_course_premium(course_id): 
        if courses_service.number_premium_courses_par_student(user_id)==5:
            return Conflict409('The student can not enroll in more than 5 premium courses.')

    if users_service.subscribe_to_course(user_id, course_id):
        data = users_service.get_teacher_info_with_course_id(course_id)

        teacher_email = data[0][0]
        teacher_first_name = data[0][1]
        teahcer_last_name = data[0][2]
        class_name = data[0][3]

        verification_link =f"http://localhost:8000/users/{user_id}/teacher_approval/{course_id}"

        users_service.send_student_enrolled_in_course_email_to_teacher(teacher_email, verification_link, teacher_first_name, teahcer_last_name, class_name)
    
        return OK200("You have enrolled in this course. Your enrollment is pending approval by the teacher.")


@user_router.put('/{user_id}/courses/{course_id}/unsubscribe', tags=['Users'])
def unsubscribe_from_course(user_id: int, course_id: int, authorization: str = Header(None)):
    '''Student unsubscribe from this course'''
    if authorization is None:
        raise Exception403Forbidden()
    
    if not courses_service.is_student_enrolled_in_course(course_id, user_id): #check if student enrolled in course
        return Conflict409('This student is not enrolled in this course.')
    
    user = get_user_or_raise_401(authorization)

    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')

    if user is None:
        raise Exception404NotFound(f"User {user_id} does not exist")
    
    if not user.id == user_id:
        raise Exception403Forbidden()

    if users_service.unsubscribe_from_course(user_id, course_id):
        return OK200("You have been unsubscribed from this course.")
    return InternalServerError500('Something went wrong.Try again.')


@user_router.get('/', tags=['Users'], response_model=User)
def view_user(authorization: str = Header()) -> User:
    ''' View account information depending on role - student or teacher or admin'''
    if authorization is None:
        raise Exception403Forbidden()

    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    if user.is_student():
        return user
    elif user.is_teacher():
        return users_service.view_teacher(user) 

@user_router.put('/', tags=['Users']) 
def update_user(update_info: UpdateData, authorization: str = Header(None)):
    '''Edit account information'''

    if authorization is None:
        raise Exception403Forbidden()
    
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    if user.is_student() and (update_info.phone or update_info.linked_in_account):
        return Forbidden403("You can not change phone or linked account")

    if users_service.update_user(user, update_info):
        return OK200("You have updated your profile successfully")
    else:
        return BadRequest400("Failed to update profile")

@user_router.get('/all', tags=['Users'])
def view_all_users_by_admin(email: str = None,
                            last_name: str = None, authorization: str = Header(None)):
    '''View all users by admin'''
    if authorization is None:
        raise Exception403Forbidden()
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        return users_service.view_admin(email, last_name) 
    return Forbidden403('You are not an administator.')

@user_router.put('/{user_id}/admin_approvals', tags=['Users'])
def admin_approves_users(user_id: int, authorization: str = Header(None)):
    '''Admin approves user role'''
    
    if authorization is None:
        raise Exception403Forbidden()
    
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        if users_service.admin_approves_user(user_id):
            return OK200('The user is approved.')
        return Conflict409('Something went wrong.Try again.')
    return Forbidden403('You are not an administator.')

@user_router.put('/{user_id}/admin_disapprovals', tags=['Users'])
def admin_disapproves_users(user_id: int, authorization: str = Header(None)):
    '''Admin disapproves user role'''
    
    if authorization is None:
        raise Exception403Forbidden()
    
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        if users_service.admin_disapproves_user(user_id):
            return OK200('The user is disapproved.')
        return InternalServerError500('Something went wrong.Try again.')
    
    return Forbidden403('You are not an administator.')

@user_router.put('/{student_id}/teacher_approval/{course_id}', tags=['Users'])
def teacher_approves_enrollment_from_student(student_id: int, course_id:int, authorization: str = Header(None)):
    '''Teacher approves enrollment from a student for their course'''
    if authorization is None:
        raise Exception403Forbidden()
    
    if not courses_service.course_exists(course_id): # check if course exists
        return NotFound404('This course does not exist.')
    
    if not users_service.find_by_id(student_id): #check if user exists
        return NotFound404('This user does not exist.')
    
    if not courses_service.is_student_enrolled_in_course(course_id, student_id): #check if student enrolled in course
        return Conflict409('This student is not enrolled in this course.')
    
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    teacher_email=users_service.get_teacher_info_with_course_id(course_id)[0][0]
    teacher=users_service.find_by_email(teacher_email)
    if teacher:
        if teacher.id == user.id:#check if teacher is course owner
            if users_service.approve_enrollment(student_id, course_id):
                return OK200('The student enrollement is approved.')
    return Forbidden403('You are not a teacher or do not own this course.')


@user_router.get('/pending_approval/students/{teacher_id}', tags=['Users'])
def view_all_pending_approval_students(teacher_id:int, authorization: str = Header(None)):
    ''' Teacher views pending approval for his/her course'''
    if authorization is None:
        raise Exception403Forbidden()
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return Conflict409('Your role is still not approved.')
    
    if user.is_teacher():
        return users_service.view_all_pending_approval_students(teacher_id)
    return Forbidden403('You are not a teacher.')