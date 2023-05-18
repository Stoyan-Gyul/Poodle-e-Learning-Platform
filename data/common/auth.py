from services.users_service import validate_token
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def get_user_params_or_raise_error(token: str) -> list:
    token_params=validate_token(token)
    if not token_params:
        raise HTTPException(status_code=401, detail="Problem with the authentication. Try Again!")

    return token_params
    