from pydantic import BaseModel, constr, condecimal
from data.common.constants import CourseStatus, CourseType, Regex

class Course(BaseModel):
    id: int | None
    title: constr(min_length=1)
    description: constr(min_length=1)
    home_page_pic: bytes | None
    course_rating: float | None
    owner_id: int | None
    is_active: constr(regex=Regex.ACTIVE_HIDDEN)
    is_premium: constr(regex=Regex.PREMIUM_PUBLIC)
    tags: list[str] | None
    objectives: list[str] | None

    @classmethod
    def from_query_result(cls, id, title, description, home_page_pic, course_rating, owner_id, is_active, is_premium, tags, objectives):
        return cls(
            id=id,
            title=title,
            description=description,
            home_page_pic=home_page_pic,
            course_rating=course_rating,
            owner_id=owner_id,
            is_active=CourseStatus.ACTIVE if is_active else CourseStatus.HIDDEN,
            is_premium=CourseType.PREMIUM if is_premium else CourseType.PUBLIC,
            tags=tags, 
            objectives=objectives,
            )