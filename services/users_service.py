from data.models import User
from data.database import read_query, insert_query, update_query
import bcrypt
from fastapi import HTTPException, status

main_salt = bcrypt.gensalt()

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
    
    sql = "SELECT * FROM users WHERE username = ?;"
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