from pydantic import BaseModel, constr, condecimal
from data.common.constants import Regex, StudentStatus

class StatusLevelMaps:
    INT_TO_STR = {0: StudentStatus.UNSUBSCRIBED, 1: StudentStatus.PENDING, 2: StudentStatus.SUBSCRIBED}
    STR_TO_INT = {StudentStatus.UNSUBSCRIBED: 0, StudentStatus.PENDING: 1, StudentStatus.SUBSCRIBED: 2}


class Report(BaseModel):
    user_id: int
    course_id: int | None
    status: constr(regex=Regex.UNSUBSCRIBED_SUBSCRIBED)
    rating: condecimal(decimal_places=1, ge=1, le=10) | None
    progress: condecimal(decimal_places=0, ge=0, le=100) | None
    first_name: str | None
    last_name: str | None
    title: str | None

    @classmethod
    def from_query_result(cls, user_id, course_id, status, rating, progress, first_name, last_name, title):
        return cls(
            user_id=user_id,
            course_id=course_id,
            status=StatusLevelMaps.INT_TO_STR[status],
            rating=rating,
            progress=progress if progress is not None else 0,
            first_name=first_name,
            last_name=last_name,
            title=title
            )