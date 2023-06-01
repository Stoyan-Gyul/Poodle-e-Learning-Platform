from pydantic import BaseModel, constr, condecimal, validator
from data.database import read_query
from typing import Optional
from data.common.constants import CourseStatus, CourseType, Role, StudentStatus, Regex


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
    home_page_pic: bytes | None
    owner_id: int
    is_active: constr(regex=Regex.ACTIVE_HIDDEN)
    is_premium: constr(regex=Regex.PREMIUM_PUBLIC)
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
            is_active=CourseStatus.ACTIVE if is_active else CourseStatus.HIDDEN,
            is_premium=CourseType.PREMIUM if is_premium else CourseType.PUBLIC,
            expertise_area = expertise_area,
            objective = objective
            )


class CourseUpdate(BaseModel):
    title: constr(min_length=1) | None
    description: constr(min_length=1) | None
    home_page_pic: None
    is_active: constr(regex=Regex.ACTIVE_HIDDEN) | None
    is_premium: constr(regex=Regex.PREMIUM_PUBLIC) | None

    @classmethod
    def from_query_result(cls, title, description, home_page_pic, is_active, is_premium):
        return cls(
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            is_active=CourseStatus.ACTIVE if is_active else CourseStatus.HIDDEN,
            is_premium=CourseType.PREMIUM if is_premium else CourseType.PUBLIC
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
    INT_TO_STR = {0: StudentStatus.UNSUBSCRIBED, 1: StudentStatus.PENDING, 2: StudentStatus.UNSUBSCRIBED}
    STR_TO_INT = {StudentStatus.UNSUBSCRIBED: 0, StudentStatus.PENDING: 1, StudentStatus.UNSUBSCRIBED: 2}

class Report(BaseModel):
    user_id: int
    course_id: int | None
    status: constr(regex=Regex.UNSUBSCRIBED_SUBSCRIBED)
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

# class TeacherAdds(BaseModel):
#     phone_number: str | None
#     linked_in_account: str | None
    

    @classmethod
    def from_query_result(cls, phone_number, linked_in_account):
        return cls(
            phone_number=phone_number,
            linked_in_account=linked_in_account
            )

class ViewPublicCourse(BaseModel):
    id: int | None
    title: str
    description: str
    course_rating: float | None
    expertise_area: str

    @classmethod
    def from_query_result(cls, id, title, description, course_rating, expertise_area):
        return cls(
            id=id,
            title=title,
            description=description,
            course_rating=course_rating,
            expertise_area=expertise_area
            )
    
class ViewStudentCourse(BaseModel):
    id: int
    title: str
    description: str
    course_rating: float | None
    home_page_pic: bytes | None
    expertise_area: str
    objective: str
    progress: float | None

    @classmethod
    def from_query_result(cls, id, title, description, course_rating, home_page_pic, expertise_area, objective, progress):
        return cls(
            id=id,
            title=title,
            description=description,
            course_rating=course_rating,
            home_page_pic=home_page_pic,
            expertise_area=expertise_area,
            objective=objective,
            progress=progress
            )
    
class ViewTeacherCourse(BaseModel):
    id: int
    title: str
    description: str
    course_rating: float | None
    home_page_pic: bytes | None
    is_active: str
    is_premium: str
    expertise_area: str
    objective: str
    
    @classmethod
    def from_query_result(cls, id, title, description, course_rating, home_page_pic, is_active, is_premium, expertise_area, objective):
        return cls(
            id=id,
            title=title,
            description=description,
            course_rating=course_rating,
            home_page_pic=home_page_pic,
            is_active=CourseStatus.ACTIVE if is_active else CourseStatus.HIDDEN,
            is_premium=CourseType.PREMIUM if is_premium else CourseType.PUBLIC,
            expertise_area=expertise_area,
            objective=objective
            )


class ViewAdminCourse(BaseModel):
    id: int
    title: str
    description: str
    course_rating: float | None
    home_page_pic: bytes | None
    is_active: str
    is_premium: str
    expertise_area: str
    objective: str
    number_students: int
    
    @classmethod
    def from_query_result(cls, id, title, description, course_rating, home_page_pic, is_active, is_premium, expertise_area, objective, number_students):
        return cls(
            id=id,
            title=title,
            description=description,
            course_rating=course_rating,
            home_page_pic=home_page_pic,
            is_active=CourseStatus.ACTIVE if is_active else CourseStatus.HIDDEN,
            is_premium=CourseType.PREMIUM if is_premium else CourseType.PUBLIC,
            expertise_area=expertise_area,
            objective=objective,
            number_students=number_students
            )

class ViewUserCourse(BaseModel):
    user_id: int
    user_first_name: str
    user_last_name: str
    course_id: int
    course_title: str

    @classmethod
    def from_query_result(cls, user_id, user_first_name, user_last_name, course_id, course_title):
        return cls(user_id=user_id, user_first_name=user_first_name, user_last_name=user_last_name, course_id=course_id, course_title=course_title)
    
class UserRating(BaseModel):
    student_email: str
    rating: int | None

    @classmethod
    def from_query_result(cls, student_email, rating):
        return cls(student_email=student_email, 
                   rating=rating)