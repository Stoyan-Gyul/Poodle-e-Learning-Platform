from fastapi import APIRouter, HTTPException, Header, Response, status
from fastapi.responses import JSONResponse, FileResponse
from data.models import User, LoginData, UpdateData, TeacherAdds, Course
from services import users_service
from services.users_service import Teacher
from data.common.auth import get_user_params_or_raise_error, get_user_or_raise_401, is_user_approved_by_admin
import uuid

user_router = APIRouter(prefix="/users")


@user_router.post("/", status_code=201, tags=['Users'])
def register_user(user: User):

    if not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password cannot be empty!")
    
    existing_user = users_service.find_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists!")
    
    if user.role is None:
        user.role = 'student'

    try:

        verification_token = str(uuid.uuid4())
        user.verification_token = verification_token

        verification_link =f"http://localhost:8000/users/{user.email}/verification/{verification_token}"

        users_service.create_new_user(user)
        
        users_service.send_verification_email(user.email, verification_link)

        return JSONResponse(status_code=201, content={'message': 'You registered successfully. Check your email for verification.'})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")
    
@user_router.get("/{email}/verification/{token}", tags=['Users'])
def verify_email(email:str, token: str):

    if users_service.verify_email(email, token):
        return JSONResponse(status_code=200, content={'message': 'User verified successfully.'})
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid verification token.")
    
@user_router.post('/login', tags=['Users'])
def login(data: LoginData):

    if data.email is None or data.password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or password cannot be empty!")
    
    user = users_service.find_by_email(data.email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email does not exist!") 


    if users_service.try_login(user, data.password):
        token = users_service.generate_token(user)
        return JSONResponse(status_code=200, content={'token': token})
    else:
        return JSONResponse(status_code=400, content={'message': 'Invalid login data'})

@user_router.put('/{user_id}/courses/{course_id}/subscribe', tags=['Users'])
def subscribe_to_course(user_id: int, course_id: int, authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=403)
    
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    user_info = users_service.validate_token(token)

    # Verify if role is approved
    if not is_user_approved_by_admin(user_info[0]):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})

    if not user_info:
        raise HTTPException(status_code=403)
    
    if not user_info[0] == user_id:
        raise HTTPException(status_code=403)
    
    user = users_service.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")

    #course = courses_service.find_by_id(course_id)
    # if course is None:
    #     raise HTTPException(status_code=404, detail=f"Course {course_id} does not exist")
    
    if users_service.subscribe_to_course(user_id, course_id):
        data = users_service.get_teacher_info_with_course_id(course_id)

        teacher_email = data[0][0]
        teacher_first_name = data[0][1]
        teahcer_last_name = data[0][2]
        class_name = data[0][3]

        verification_link =f"http://localhost:8000/users/{user_id}/approval/{course_id}"

        users_service.send_student_enrolled_in_course_email_to_teacher(teacher_email, verification_link, teacher_first_name, teahcer_last_name, class_name)
    
        return Response(content = "You have enrolled in this course. Your enrollment is pending approval by the teacher.", status_code=200)

@user_router.put('/{user_id}/courses/{course_id}/unsubscribe', tags=['Users'])
def unsubscribe_from_course(user_id: int, course_id: int, authorization: str = Header(None)):
    
    if authorization is None:
        raise HTTPException(status_code=403)
    
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    user_info = users_service.validate_token(token)

    # Verify if role is approved
    if not is_user_approved_by_admin(user_info[0]):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})

    if not user_info:
        raise HTTPException(status_code=403)
    
    if not user_info[0] == user_id:
        raise HTTPException(status_code=403)
    
    user = users_service.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")

    #course = courses_service.find_by_id(course_id)
    # if course is None:
    #     raise HTTPException(status_code=404, detail=f"Course {course_id} does not exist")

    users_service.unsubscribe_from_course(user_id, course_id)
    return Response(content="You have been unsubscribed from this course.", status_code=200)

@user_router.get('/', tags=['Users'], response_model=User)
def view_user(authorization: str = Header()) -> User | Teacher:
    ''' View account information depending on role - student or teacher or admin'''
    if authorization is None:
        raise HTTPException(status_code=403)

    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})
    
    if user.is_student():
        return user
    elif user.is_teacher():
        return users_service.view_teacher(user) 

@user_router.put('/', tags=['Users']) 
def update_user(update_info: UpdateData, authorization: str = Header(None)):
    '''Edit account information'''

    if authorization is None:
        raise HTTPException(status_code=403)
    
    user = get_user_or_raise_401(authorization)
    # Verify if role is approved
    if not is_user_approved_by_admin(user.id):
        return JSONResponse(status_code=409, content={'detail': 'Your role is still not approved.'})
    
    if user.is_student() and (update_info.phone or update_info.linked_in_account):
        return JSONResponse(content="You can not change phone or linked account", status_code=401)

    if users_service.update_user(user, update_info):
        return JSONResponse(content="You have updated your profile successfully", status_code=200)
    else:
        return JSONResponse(content="Failed to update profile", status_code=400)

@user_router.get('/all', tags=['Users'])
def view_all_users_by_admin(email: str = None,
                            last_name: str = None, authorization: str = Header(None)):
    '''View all users by admin'''
    if authorization is None:
        raise HTTPException(status_code=403)
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        return users_service.view_admin(email, last_name) 
    return JSONResponse(status_code=409, content={'detail': 'You are not administator.'})

@user_router.put('/{user_id}/admin_approvals', tags=['Users'])
def admin_approves_users(user_id: int, authorization: str = Header(None)):
    '''Admin approves user role'''
    
    if authorization is None:
        raise HTTPException(status_code=403)
    
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        if users_service.admin_approves_user(user_id):
            return JSONResponse(status_code=200, content={'message': 'The user is approved.'})
        return JSONResponse(status_code=409, content={'detail': 'Something went wrong.Try again.'})
    return JSONResponse(status_code=409, content={'detail': 'You are not administator.'})

@user_router.put('/{user_id}/admin_disapprovals', tags=['Users'])
def admin_approves_users(user_id: int, authorization: str = Header(None)):
    '''Admin disapproves user role'''
    
    if authorization is None:
        raise HTTPException(status_code=403)
    
    user = get_user_or_raise_401(authorization)
    if user.is_admin():
        if users_service.admin_disapproves_user(user_id):
            return JSONResponse(status_code=200, content={'message': 'The user is disapproved.'})
        return JSONResponse(status_code=409, content={'detail': 'Something went wrong.Try again.'})
    
    return JSONResponse(status_code=409, content={'detail': 'You are not administator.'})

@user_router.put('/{student_id}/teacher_approval/{course_id}', tags=['Users'])
def teacher_approves_enrollment_from_student(student_id: int, course_id:int, autorization: str = Header(None)):
    '''Teacher approves enrollment from a student for their course'''
    #not all checks completed
    return users_service.approve_enrollment(student_id, course_id)

@user_router.get('/pending_approval/students/{teacher_id}', tags=['Users'])
def view_all_pending_approvall_students(teacher_id:int, autorization: str = Header(None)):
    #not all checks completed
    return users_service.view_all_pending_approval_students(teacher_id)