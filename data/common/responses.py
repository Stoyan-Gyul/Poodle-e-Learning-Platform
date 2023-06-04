from fastapi.responses import JSONResponse
from fastapi import status


class NoContent(JSONResponse):
    def __init__(self):
        super().__init__(status_code=status.HTTP_204_NO_CONTENT)


class BadRequest(JSONResponse):
    def __init__(self, content={}):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, content=content)


class Unauthorized(JSONResponse):
    def __init__(self, content={}):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, content=content)


class Forbidden(JSONResponse):
    def __init__(self, content={}):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, content=content)


class NotFound(JSONResponse):
    def __init__(self, content={}):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, content=content)


class Conflict(JSONResponse):
    def __init__(self, content={}):
        super().__init__(status_code=status.HTTP_409_CONFLICT, content=content)


class InternalServerError(JSONResponse):
    def __init__(self, content={}):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)
