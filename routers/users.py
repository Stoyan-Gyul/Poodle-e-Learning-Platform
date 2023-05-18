from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import JSONResponse
from data.models import User, LoginData
from services import users_service


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
    

@user_router.get('/', tags=['Users'])
def view_user(token: str =Header()):
    token_params=users_service.validate_token(token)
    if token_params:
        id=token_params[0]
        role=token_params[2]
    else:
        return JSONResponse(status_code=500, content={'detail': 'Problem with the authentication. Try Again!'} )

    user=users_service.find_by_id(id)
    
    if role == 'student':
        return user
    elif role == 'teacher':
        return users_service.view_teacher(user) 
       
