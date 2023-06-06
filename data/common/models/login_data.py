from pydantic import BaseModel

class LoginData(BaseModel):
    email: str | None
    password: str | None