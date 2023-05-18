from pydantic import BaseModel

class User(BaseModel):
    id: int | None
    email: str
    password: str
    first_name: str | None
    last_name: str | None
    role: str | None

    @classmethod
    def from_query_result(cls, id, email, password, first_name, last_name, role):
        return cls(
            id=id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role)

class LoginData(BaseModel):
    email: str | None
    password: str | None

class TeacherAdds(BaseModel):
    phone_number: str | None
    linked_in_account: str | None
    
    @classmethod
    def from_query_result(cls, phone_number, linked_in_account):
        return cls(
            phone_number=phone_number,
            linked_in_account=linked_in_account
            ) 