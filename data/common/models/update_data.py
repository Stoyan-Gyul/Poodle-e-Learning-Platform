from pydantic import BaseModel

class UpdateData(BaseModel):
    password: str | None
    first_name: str | None
    last_name: str | None
    role: str | None
    phone: str | None
    linked_in_account: str | None