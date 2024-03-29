from data.common.models.user import User
from services.users_service import find_by_id, validate_token
from fastapi import HTTPException
from data.common.exceptions import Exception401Unauthorized
from fastapi import status
from data.database import read_query


def get_user_params_or_raise_error(token: str) -> list:
    token_params=validate_token(token)
    if not token_params:
        raise Exception401Unauthorized("Problem with the authentication. Try Again!")

    return token_params


def get_user_or_raise_401(authorization: str) -> User:
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None

    token_params=validate_token(token)
    if not token_params:
        raise Exception401Unauthorized("Problem with the authentication. Try Again!")
    
    user_id = token_params[0]
    user = find_by_id(user_id)

    return user


def is_user_approved_by_admin(user_id: int)->bool:
    ''' Verify is user role is approved'''
    sql='''SELECT is_approved FROM users WHERE id=?'''
    if read_query(sql,(user_id,))[0][0]:
        return True
    return False