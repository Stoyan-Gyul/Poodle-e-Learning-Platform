from fastapi.responses import JSONResponse
from fastapi import status

class CustomJSONResponse(JSONResponse):
    def __init__(self, status_code: int, message: str = None, content: dict = None, key: str = "detail"):
        if message is not None:
            content = {key: message}
        super().__init__(status_code=status_code, content=content)

class OK_200(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_200_OK, message=message, content=content, key="message")

class Created_201(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_201_CREATED, message=message, content=content, key="message")

class NoContent_204(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_204_NO_CONTENT, message=message, content=content, key="message")

class BadRequest_400(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, content=content)

class Unauthorized_401(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message, content=content)

class Forbidden_403(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message, content=content)

class NotFound_404(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message, content=content)

class Conflict_409(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message, content=content)

class InternalServerError_500(CustomJSONResponse):
    def __init__(self, message=None, content=None):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, content=content)
