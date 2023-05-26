from data.models import User, TeacherAdds, UpdateData, ViewUser
from pydantic import BaseModel
from data.database import read_query, insert_query, update_query
import bcrypt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import jwt
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Teacher(BaseModel):
    user: User
    teacher_adds: TeacherAdds

main_salt = bcrypt.gensalt()
secret_key = secrets.token_hex(32)
expiration_time = timedelta(minutes=300)

def find_by_id(id: int) -> User | None:
    if id is None:
        return None
    
    sql = "SELECT id, email, password, first_name, last_name, role FROM users WHERE id = ?;"
    sql_params = (id,)
    data = read_query(sql, sql_params)

    if data:
        return User.from_query_result(*data[0])
    else:
        return None

def find_by_email(email: str) -> User | None:

    if email is None:
        return None
    
    sql = "SELECT id, email, password, first_name, last_name, role FROM users WHERE email = ?;"
    sql_params = (email,)
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
    is_verified = 0

    sql_user = "INSERT INTO users (email, password, role, first_name, last_name, verification_token, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?);"
    sql_params_user = (user.email, hashed_password, user.role, user.first_name, user.last_name, user.verification_token, is_verified)
        
    user_id = insert_query(sql_user, sql_params_user)

    if user.phone or user.linked_in_account:
    
        sql_teacher = "INSERT INTO teachers (users_id, phone_number, linked_in_account) VALUES (?, ?, ?)"
        sql_params_teacher = (user_id, user.phone, user.linked_in_account)
        
        insert_query(sql_teacher, sql_params_teacher)
        
    return user_id

def try_login(user: User, password: str) -> User | None:
    if user is None or password is None:
        return None
    
    pass_match = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
    
    if user and pass_match:
        return user

def generate_token(user: User) -> str:
    if user is None:
        return None
    
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
    if user_id is None or course_id is None:
        return None
    
    sql = "INSERT INTO users_have_courses (users_id, courses_id, status) VALUES (?, ?, ?)"
    sql_params = (user_id, course_id, 0)

    return update_query(sql, sql_params)

def unsubscribe_from_course(user_id: int, course_id:int):
    if user_id is None or course_id is None:
        return None
    
    sql = "UPDATE users_have_courses SET status = ? WHERE users_id = ? AND courses_id = ?"
    sql_params = (2, user_id, course_id)

    return update_query(sql, sql_params)

def view_teacher(user: User)-> User | Teacher:
    ''' View account information as per the role -  teacher'''

    id=user.id
    sql = "SELECT phone_number, linked_in_account FROM teachers WHERE users_id = ?;"
    sql_params = (id,)
    data = read_query(sql, sql_params)
    if data:
        teacher_adds=TeacherAdds.from_query_result(*data[0])
        # return Teacher(user=user, teacher_adds=teacher_adds)
        return User(id=user.id,
                    email=user.email,
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role=user.role,
                    phone=data[0][0],
                    linked_in_account=data[0][1])
    else:
        return user
    
def update_user(user: User, update_info: UpdateData) -> bool | None:
    ''' Edit basic account information'''

    if user is None or update_info is None:
        return None
    
    hashed_password=''
    if update_info.password:
        passwd = update_info.password.encode("utf-8")
        hashed_password = bcrypt.hashpw(passwd, main_salt)

    merged=User(
        id=user.id,
        email=user.email,
        password=hashed_password or user.password,
        first_name=update_info.first_name or user.first_name,
        last_name=update_info.last_name or user.last_name,
        role=user.role)
    
    if update_info.phone:

        update_query('''UPDATE teachers SET
                    phone_number = ? 
                    WHERE users_id = ?''',
                    (update_info.phone, merged.id))
        
    if update_info.linked_in_account:

        update_query('''UPDATE teachers SET
                    linked_in_account = ? 
                    WHERE users_id = ?''',
                    (update_info.linked_in_account, merged.id))
        
    return update_query('''UPDATE users SET
                    password = ?, first_name = ?, last_name = ?, role = ?
                    WHERE id = ?''',
                    (merged.password, merged.first_name, merged.last_name, merged.role, merged.id))

# def is_course_owner(user_id, course_id: int):
#         owner_id = read_query('''SELECT owner_id FROM courses
# WHERE id = ?''', (course_id,))
#         return user_id == owner_id

def send_verification_email(email: str, verification_link: str):
    smtp_host = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "poodle.learning@outlook.com"
    smtp_password = "1234@alpha"  # Use your Outlook.com account password

    message = MIMEMultipart()
    message["From"] = "poodle.learning@outlook.com"
    message["To"] = email
    message["Subject"] = "Account Verification"

    body = f"Please click the following link to verify your account: {verification_link}"
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(message["From"], message["To"], message.as_string())

        return("Verification email sent successfully.")

def verify_email(email:str, token:str) -> bool:
    if email is None or token is None:
        return None
    
    sql = "SELECT verification_token FROM users WHERE email = ?"
    sql_params = (email,)

    actual_token_tuple = read_query(sql, sql_params)[0]
    actual_token = actual_token_tuple[0]

    if actual_token == token:
        sql = "UPDATE users SET is_verified = ? WHERE email = ?"
        sql_params = (1, email)

        return update_query(sql, sql_params)
    else:
        return False

def view_current_user_info(id:int, role: str):
    if id is None or role is None:
        return None
    
    if role == 'student':
        sql = "SELECT first_name, last_name, role FROM users WHERE id = ?;"
        sql_params = (id,)
        data = read_query(sql, sql_params)

        if data:
            return ViewUser(first_name=data[0][0], last_name=data[0][1], role=data[0][2])
        else:
            return None
    elif role == 'teacher':
        sql = "SELECT users.first_name, users.last_name, users.role, teachers.phone_number, teachers.linked_in_account FROM users JOIN teachers ON users.id = teachers.users_id WHERE users.id = ?"
        sql_params = (id,)
        data = read_query(sql, sql_params)

        if data:
            return ViewUser(first_name=data[0][0], last_name=data[0][1], role=data[0][2], phone=data[0][3], linked_in_account=data[0][4])
        else:
            return None