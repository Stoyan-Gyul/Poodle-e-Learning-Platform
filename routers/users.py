from fastapi import APIRouter, HTTPException, Header, Response, status, Header
from fastapi.responses import JSONResponse
from data.models import User, LoginData, TeacherAdds, Course
from services import users_service, courses_service
from services.users_service import Teacher
from data.common.auth import get_user_params_or_raise_error


user_router = APIRouter(prefix="/users")


@user_router.post("/", status_code=201)
def register_user(user: User):

    if not user.email or not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or password cannot be empty!")
    
    existing_user = users_service.find_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists!")
    
    if user.role is None:
        user.role = 'user'

    try:
        created_user_id = users_service.create_new_user(user)
        return JSONResponse(status_code=201, content={'message': f'User with id {created_user_id} created'})
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong!")
    

@user_router.post('/login')
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


@user_router.put('/{user_id}/courses/{course_id}/subscribe')
def subscribe_to_course(user_id: int, course_id: int, authorization: str = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=403)
    
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    user_info = users_service.validate_token(token)
    if not user_info:
        raise HTTPException(status_code=403)
    
    if not user_info[0] == user_id:
        raise HTTPException(status_code=403)
    
    user = users_service.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")

    course = courses_service.find_by_id(course_id)
    # if course is None:
    #     raise HTTPException(status_code=404, detail=f"Course {course_id} does not exist")
    
    
    users_service.subscribe_to_course(user_id, course_id)
    return Response(content = "You have subscribed to this course", status_code=200,)

@user_router.put('/{user_id}/courses/{course_id}/unsubscribe')
def unsubscribe_from_course(user_id: int, course_id: int, authorization: str = Header(None)):
    
    if authorization is None:
        raise HTTPException(status_code=403)
    
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    user_info = users_service.validate_token(token)
    if not user_info:
        raise HTTPException(status_code=403)
    
    if not user_info[0] == user_id:
        raise HTTPException(status_code=403)
    
    user = users_service.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} does not exist")

    course = courses_service.find_by_id(course_id)
    # if course is None:
    #     raise HTTPException(status_code=404, detail=f"Course {course_id} does not exist")

    users_service.unsubscribe_from_course(user_id, course_id)
    return Response(content="You have been unsubscribed from this course.", status_code=200)


@user_router.get('/', tags=['Users'], response_model=User)
def view_user(token: str =Header()) -> User | Teacher:
    ''' View account information depending on role - student or teacher'''

    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    user=users_service.find_by_id(id)
    
    if role == 'student':
        return user
    elif role == 'teacher':
        return users_service.view_teacher(user) 


@user_router.put('/', tags=['Users'], response_model=User | Teacher)
def update_user(user: User, teacher_adds: TeacherAdds = None, token: str =Header()):
    '''Edit account information depending on role - sutdent or teacher'''

    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    existing_user=users_service.find_by_id(id)

    if role == 'student':
        return users_service.update_user(existing_user, user)
    elif role == 'teacher':
        if teacher_adds:
            return users_service.update_teacher(existing_user, user, teacher_adds)
        else:
            return users_service.update_user(existing_user, user)


@user_router.get('/enrolled_courses', tags=['Users'], response_model=list[Course])
def view_enrolled_courses(token: str =Header()) -> list[Course]:
    ''' View enrolled courses by students only'''

    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    

    if role == 'student':
        return JSONResponse(status_code=200,content={'message': 'This for test ONLY!Students Enrolled Courses.'} )
        # return users_service.enrolled_courses(id)
    else:
        return JSONResponse(status_code=409,content={'detail': 'Only students can view their enrolled courses!'} )
    

@user_router.get('/courses', tags=['Users'])
def view_all_courses(token: str =Header()):
    ''' View all courses depending on role - anonymous, student, teacher'''
    if not token:
        return courses_service.view_public_courses()
        # return JSONResponse(status_code=200,content={'message': 'This for test ONLY Anonymous users!'})
    
    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    
    if role == 'student':
        # return public_and_enrolled_courses(id)
        return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Students'} )
    elif role == 'teacher':
        # return all_courses_and_sections(id)
        return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Teachers'})
    # elif role == 'admin':
    #     return JSONResponse(status_code=200,content={'message': 'This for test ONLY! Admin'} )
    
@user_router.put('/course_ratings', tags=['Users'])
def course_rating(token: str =Header()):
    token_params=get_user_params_or_raise_error(token)
    
    id=token_params[0]
    role=token_params[2]
    

    if role == 'student':
        return JSONResponse(status_code=200,content={'message': 'This for test ONLY!Students rate courses'} )
        # return users_service.rating_course(id)
    else:
        return JSONResponse(status_code=409,content={'detail': 'Only students can rate their enrolled courses!'} )



    
       
