from pydantic import BaseModel, constr

class Tag(BaseModel):
    id: int | None
    expertise_area: constr(min_length=1)

    @classmethod
    def from_query_result(cls, id, expertise_area):
        return cls(
            id=id,
            expertise_area=expertise_area
        )
    