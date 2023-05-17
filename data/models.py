from pydantic import BaseModel, constr

class User(BaseModel):
    id: int | None
    email: str
    password: str
    first_name: str | None
    last_name: str | None
    role: str | None

    @classmethod
    def from_query_result(cls, id, email, password, first_name, last_name, role):
        return cls(
            id=id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role)

class LoginData(BaseModel):
    email: str | None
    password: str | None


class StatusLevelMaps:
    INT_TO_STR = {0: 'unsubscribed', 1: 'pending', 2: 'subscribed'}
    STR_TO_INT = {'unsubscribed': 0, 'pending': 1, 'subscribed': 2}

class Course(BaseModel):
    id: int | None
    title: constr(min_length=1)
    description: constr(min_length=1)
    status: constr(regex='^unsubscribed|pending|subscribed$')
    owner_id: int
    is_active: constr(regex='^active|hidden$')

    @classmethod
    def from_query_result(cls, id, title, description, status, owner_id, is_active):
        return cls(
            id=id,
            title=title,
            description=description,
            status=StatusLevelMaps.INT_TO_STR[status],
            owner_id=owner_id,
            is_active='active' if is_active else 'hidden'
            )


class Section(BaseModel):
    id: int | None
    title: constr(min_length=1)
    content_type: str
    description: constr(min_length=1)
    external_link: constr(min_length=1)
    courses_id: int

    @classmethod
    def from_query_result(cls, id, title, content_type, description, external_link, courses_id):
        return cls(
            id=id,
            title=title,
            description=description,
            content_type=content_type,
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