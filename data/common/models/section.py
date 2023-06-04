from pydantic import BaseModel, constr, condecimal
from typing import Optional


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