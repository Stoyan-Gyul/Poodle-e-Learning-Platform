from pydantic import BaseModel
from data.common.constants import Role
from data.common.models.course import Course


class User(BaseModel):
    id: int | None
    email: str
    password: str
    first_name: str | None
    last_name: str | None
    role: str | None
    phone: int | None
    linked_in_account: str | None
    verification_token: str | None
    is_verified: str | None
    is_approved: str | None

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_teacher(self):
        return self.role == Role.TEACHER

    def is_student(self):
        return self.role == Role.STUDENT

    def is_course_owner(self, course: Course):
        return self.id == course.owner_id

    @classmethod
    def from_query_result(cls, id, email, password, first_name, last_name, role):
        return cls(
            id=id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role)
    
    @classmethod
    def from_query_result_for_admin(cls, id, email, password, first_name, last_name, role, phone, linked_in_account, verification_token, is_verified, is_approved):
        return cls(
            id=id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone=phone,
            linked_in_account=linked_in_account,
            verification_token=verification_token,
            is_verified='verified' if is_verified else 'non verified',
            is_approved='approved' if is_approved else 'non approved')