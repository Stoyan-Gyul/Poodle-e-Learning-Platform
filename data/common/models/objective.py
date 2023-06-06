from pydantic import BaseModel, constr

class Objective(BaseModel):
    id: int | None
    description: constr(min_length=1)

    @classmethod
    def from_query_result(cls, id, description):
        return cls(
            id=id,
            description=description
            )
