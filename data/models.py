from pydantic import BaseModel, constr, condecimal
from data.database import read_query

class Role:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'


class User(BaseModel):
    id: int | None
    email: str
    password: str
    first_name: str | None
    last_name: str | None
    role: str | None

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_teacher(self):
        return self.role == Role.TEACHER

    def is_student(self):
        return self.role == Role.STUDENT

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


class Course(BaseModel):
    id: int | None
    title: constr(min_length=1)
    description: constr(min_length=1)
    home_page_pic: None
    owner_id: int
    is_active: constr(regex='^active|hidden$')

    @classmethod
    def from_query_result(cls, id, title, description, home_page_pic, owner_id, is_active):
        return cls(
            id=id,
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            owner_id=owner_id,
            is_active='active' if is_active else 'hidden'
            )


class Section(BaseModel):
    id: int | None
    title: constr(min_length=1)
    content_type: str
    description: constr(min_length=1)
    external_link: constr(min_length=1)
    courses_id: int

    @classmethod
    def from_query_result(cls, id, title, content_type, description, external_link, courses_id):
        return cls(
            id=id,
            title=title,
            description=description,
            content_type=content_type,
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
    INT_TO_STR = {0: 'unsubscribed', 1: 'pending', 2: 'subscribed'}
    STR_TO_INT = {'unsubscribed': 0, 'pending': 1, 'subscribed': 2}

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
    title: str
    description: str
    home_page_pic: None
    expertise_area: str
    objective: str
    
    @classmethod
    def from_query_result(cls, title, description, home_page_pic, expertise_area, objective):
        return cls(
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            expertise_area=expertise_area,
            objective=objective
            )