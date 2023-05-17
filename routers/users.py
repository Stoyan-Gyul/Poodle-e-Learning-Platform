from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from data.models import User, LoginData, UpdateUserData
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