from fastapi import APIRouter, HTTPException, Header, Response, status
from fastapi.responses import JSONResponse
from data.models import User, LoginData
from services import users_service, courses_service


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