from pydantic import BaseModel
from data.common.constants import CourseStatus, CourseType

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
    def from_query_result(cls, id, title, description, course_rating, home_page_pic, expertise_area, objective, progress=None):
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