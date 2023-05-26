from pydantic import BaseModel, constr, condecimal, validator
from data.database import read_query
from typing import Optional

class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

class Status:
    UNSUBSCRIBED = 'unsubscribed'
    PENDING = 'pending'
    SUBSCRIBED = 'subscribed'


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

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_teacher(self):
        return self.role == Role.TEACHER

    def is_student(self):
        return self.role == Role.STUDENT

    def is_course_owner(self, course: 'Course'):
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

class UpdateData(BaseModel):
    password: str | None
    first_name: str | None
    last_name: str | None
    role: str | None
    phone: str | None
    linked_in_account: str | None

class LoginData(BaseModel):
    email: str | None
    password: str | None


class Course(BaseModel):
    id: int | None
    title: constr(min_length=1)
    description: constr(min_length=1)
    home_page_pic: None
    owner_id: int
    is_active: constr(regex='^active|hidden$')
    is_premium: constr(regex='^premium|public$')
    expertise_area: str | None
    objective: str | None

    @classmethod
    def from_query_result(cls, id, title, description, home_page_pic, owner_id, is_active, is_premium, expertise_area, objective):
        return cls(
            id=id,
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            owner_id=owner_id,
            is_active='active' if is_active else 'hidden',
            is_premium='premium' if is_premium else 'public',
            expertise_area = expertise_area,
            objective = objective
            )


class CourseUpdate(BaseModel):
    title: constr(min_length=1) | None
    description: constr(min_length=1) | None
    home_page_pic: None
    is_active: constr(regex='^active|hidden$') | None
    is_premium: constr(regex='^premium|public$') | None

    @classmethod
    def from_query_result(cls, title, description, home_page_pic, is_active, is_premium):
        return cls(
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            is_active='active' if is_active else 'hidden',
            is_premium='premium' if is_premium else 'public'
            )


class Section(BaseModel):
    id: int | None
    title: constr(min_length=1)
    content: str
    description: constr(min_length=1)
    external_link: constr(min_length=1)
    courses_id: Optional[int]

    @classmethod
    def from_query_result(cls, id, title, content, description, external_link, courses_id):
        return cls(
            id=id,
            title=title,
            description=description,
            content=content,
            external_link=external_link,
            courses_id=courses_id
            )


class Objective(BaseModel):
    id: int | None
    description = constr(min_length=1)

    @classmethod
    def from_query_result(cls, id, description):
        return cls(
            id=id,
            description=description
            )


class Tag(BaseModel):
    id: int | None
    expertise_area = constr(min_length=1)

    @classmethod
    def from_query_result(cls, id, expertise_area):
        return cls(
            id=id,
            expertise_area=expertise_area
            )


class StatusLevelMaps:
    INT_TO_STR = {0: Status.UNSUBSCRIBED, 1: Status.PENDING, 2: Status.SUBSCRIBED}
    STR_TO_INT = {Status.UNSUBSCRIBED: 0, Status.PENDING: 1, Status.SUBSCRIBED: 2}

class Report(BaseModel):
    user_id: int
    course_id: int
    status: constr(regex='^unsubscribed|pending|subscribed$')
    rating: condecimal(decimal_places=1, ge=1, le=10) | None
    progress: condecimal(decimal_places=0, ge=0, le=100) | None

    @classmethod
    def from_query_result(cls, user_id, course_id, status, rating, progress):
        return cls(
            user_id=user_id,
            course_id=course_id,
            status=StatusLevelMaps.INT_TO_STR[status],
            rating=rating,
            progress=progress if progress is not None else 0
            )

class TeacherAdds(BaseModel):
    phone_number: str | None
    linked_in_account: str | None
    

    @classmethod
    def from_query_result(cls, phone_number, linked_in_account):
        return cls(
            phone_number=phone_number,
            linked_in_account=linked_in_account
            )

class ViewPublicCourse(BaseModel):
    title: str
    description: str
    expertise_area: str

    @classmethod
    def from_query_result(cls, title, description, expertise_area):
        return cls(
            title=title,
            description=description,
            expertise_area=expertise_area
            )
    
class ViewStudentCourse(BaseModel):
    id: int
    title: str
    description: str
    home_page_pic: None
    expertise_area: str
    objective: str
    
    @classmethod
    def from_query_result(cls, id, title, description, home_page_pic, expertise_area, objective):
        return cls(
            id=id,
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            expertise_area=expertise_area,
            objective=objective
            )
class ViewTeacherCourse(BaseModel):
    id: int
    title: str
    description: str
    home_page_pic: None
    is_active: str
    is_premium: str
    expertise_area: str
    objective: str
    
    @classmethod
    def from_query_result(cls, id, title, description, home_page_pic, is_active, is_premium, expertise_area, objective):
        return cls(
            id=id,
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            is_active='active' if is_active else 'hidden',
            is_premium='premium' if is_premium else 'public',
            expertise_area=expertise_area,
            objective=objective
            )
    
class ViewUser(BaseModel):
    password: str | None
    first_name: str | None
    last_name: str | None
    role: str | None
    phone: int | None
    linked_in_account: str | None
