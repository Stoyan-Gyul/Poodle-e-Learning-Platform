from pydantic import BaseModel, constr, condecimal
from data.common.constants import Regex
from data.common.models.tag import Tag
from data.common.models.objective import Objective
from data.common.models.section import Section


class CourseResponse(BaseModel):
    id: int | None
    title: constr(min_length=1)
    description: constr(min_length=1)
    home_page_pic: bytes | None
    owner_id: int | None
    is_active: constr(regex=Regex.ACTIVE_HIDDEN)
    is_premium: constr(regex=Regex.PREMIUM_PUBLIC)
    rating: condecimal(decimal_places=1, ge=1, le=10) | None
    tags: list[Tag]
    objectives: list[Objective]
    sections: list[Section]