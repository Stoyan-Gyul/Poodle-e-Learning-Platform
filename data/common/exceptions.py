from fastapi import HTTPException
from fastapi import status

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)

class Exception400BadRequest(CustomHTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class Exception401Unauthorized(CustomHTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class Exception403Forbidden(CustomHTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class Exception404NotFound(CustomHTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class Exception500InternalServerError(CustomHTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
