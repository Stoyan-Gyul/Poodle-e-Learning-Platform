from data.models import User, TeacherAdds
from pydantic import BaseModel
from data.database import read_query, insert_query, update_query
import bcrypt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import jwt
import secrets

class Teacher(BaseModel):
    user: User
    teacher_adds: TeacherAdds

main_salt = bcrypt.gensalt()
secret_key = secrets.token_hex(32)
expiration_time = timedelta(minutes=300)

def find_by_id(id: int) -> User | None:
    if id is None:
        return None
    
    sql = "SELECT * FROM users WHERE id = ?;"
    sql_params = (id,)
    data = read_query(sql, sql_params)

    if data:
        return User.from_query_result(*data[0])
    else:
        return None

def find_by_email(username: str) -> User | None:

    if username is None:
        return None
    
    sql = "SELECT * FROM users WHERE email = ?;"
    sql_params = (username,)
    data = read_query(sql, sql_params)

    if data:
        return User.from_query_result(*data[0])
    else:
        return None

def create_new_user(user: User):
    if user is None:
        return None
    
    passwd = user.password.encode("utf-8")
    hashed_password = bcrypt.hashpw(passwd, main_salt)

    sql = "INSERT INTO users (email, password, role, first_name, last_name) VALUES (?, ?, ?, ?, ?);"
    sql_params = (user.email, hashed_password, user.role, user.first_name, user.last_name)
        
    user_id = insert_query(sql, sql_params)
    return user_id

def try_login(user: User, password: str) -> User | None:
    if user is None or password is None:
        return None
    
    pass_match = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    
    if user and pass_match:
        return user

def generate_token(user: User) -> str:
    expiry = datetime.utcnow() + expiration_time

    payload = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": expiry 
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def validate_token(token):
    if token is None:
        return None
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")
        expiration = payload.get("exp")

        if expiration is not None and datetime.utcnow() < datetime.fromtimestamp(expiration):
            # Token is not expired, return the decoded user information
            return [user_id, email, role]

        # Token has expired
        return None
    
    except jwt.ExpiredSignatureError:
        # Handle token expiration error
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token error
        return None

def subscribe_to_course(user_id: int, course_id:int):
    sql = "INSERT INTO users_have_courses (users_id, courses_id, status) VALUES (?, ?, ?)"
    sql_params = (user_id, course_id, 0)

    return update_query(sql, sql_params)

def unsubscribe_from_course(user_id: int, course_id:int):
    sql = "UPDATE users_have_courses SET status = ? WHERE users_id = ? AND courses_id = ?"
    sql_params = (2, user_id, course_id)

    return update_query(sql, sql_params)


def view_teacher(user: User)-> User | Teacher:
    id=user.id
    sql = "SELECT phone_number, linked_in_account FROM teachers WHERE users_id = ?;"
    sql_params = (id,)
    data = read_query(sql, sql_params)
    if data:
        teacher_adds=TeacherAdds.from_query_result(*data[0])
        return Teacher(user=user, teacher_adds=teacher_adds)
    else:
        return user
