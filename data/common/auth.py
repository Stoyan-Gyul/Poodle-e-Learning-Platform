from data.models import User
from services.users_service import find_by_id, validate_token
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def get_user_params_or_raise_error(token: str) -> list:
    token_params=validate_token(token)
    if not token_params:
        raise HTTPException(status_code=401, detail="Problem with the authentication. Try Again!")

    return token_params


def get_user_or_raise_401(token: str) -> User:
    token_params = get_user_params_or_raise_error(token)
    user_id = token_params[0]
    user = find_by_id(user_id)

    return user