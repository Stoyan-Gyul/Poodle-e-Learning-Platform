from pydantic import BaseModel, constr
from data.common.constants import CourseStatus, CourseType, Regex

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