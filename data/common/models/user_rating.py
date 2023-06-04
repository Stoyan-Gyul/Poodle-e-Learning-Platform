from pydantic import BaseModel

class UserRating(BaseModel):
    student_email: str
    rating: int | None

    @classmethod
    def from_query_result(cls, student_email, rating):
        return cls(student_email=student_email, 
                   rating=rating)