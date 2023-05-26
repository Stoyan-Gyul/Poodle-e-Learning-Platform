from data.models import User
from services.users_service import find_by_id, validate_token
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status


def get_user_params_or_raise_error(token: str) -> list:
    token_params=validate_token(token)
    if not token_params:
        raise HTTPException(status_code=401, detail="Problem with the authentication. Try Again!")

    return token_params


def get_user_or_raise_401(authorization: str) -> User:
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    token_params=validate_token(token)
    if not token_params:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Problem with the authentication. Try Again!")
    
    user_id = token_params[0]
    user = find_by_id(user_id)

    return user