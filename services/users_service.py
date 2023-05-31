from data.models import User, TeacherAdds, UpdateData, ViewUserCourse
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

# class Teacher(BaseModel):
#     user: User
#     teacher_adds: TeacherAdds

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
    is_approved = 0

    sql_user = "INSERT INTO users (email, password, role, first_name, last_name, verification_token, is_verified, is_approved) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    sql_params_user = (user.email, hashed_password, user.role, user.first_name, user.last_name, user.verification_token, is_verified, is_approved)
        
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
    #status 0 = sub, 1 = enrolled, 2 = unsubscribed
    sql = "INSERT INTO users_have_courses (users_id, courses_id, status) VALUES (?, ?, ?)"
    sql_params = (user_id, course_id, 0)

    return update_query(sql, sql_params)

def unsubscribe_from_course(user_id: int, course_id:int):
    if user_id is None or course_id is None:
        return None
    
    sql = "UPDATE users_have_courses SET status = ? WHERE users_id = ? AND courses_id = ?"
    sql_params = (2, user_id, course_id)

    return update_query(sql, sql_params)

def view_teacher(user: User)-> User:
    ''' View account information as per the role -  teacher'''

    id=user.id
    sql = "SELECT phone_number, linked_in_account FROM teachers WHERE users_id = ?;"
    sql_params = (id,)
    data = read_query(sql, sql_params)
    if data:
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
        
def admin_approves_user(user_id: int)->bool:
    '''Admin approves user role'''
    sql='''UPDATE users SET is_approved = 1 WHERE (`id` = ?);'''
    data=update_query(sql,(user_id,))
    if data:
        return True
    return False


def get_teacher_info_with_course_id(course_id:int) -> list: 
        if course_id is None:
            return None
        
        sql = "SELECT u.email, u.first_name, u.last_name, c.title FROM users AS u JOIN courses AS c ON u.id = c.owner_id WHERE c.id = ?"
        sql_params = (course_id,)

        data = read_query(sql, sql_params)

        return data

def send_student_enrolled_in_course_email_to_teacher(teacher_email: str, verification_link: str, teacher_first_name, teacher_last_name, class_name: str):
    smtp_host = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "poodle.learning@outlook.com"
    smtp_password = "1234@alpha" 

    message = MIMEMultipart()
    message["From"] = "poodle.learning@outlook.com"
    message["To"] = teacher_email
    message["Subject"] = "New Student Enrollment"

    body = f"Dear {teacher_first_name} {teacher_last_name},\n\n"
    body += f"A new student has enrolled in your class: '{class_name}'.\n"
    body += f"Click the following link to approve their enrollment: {verification_link}\n\n"
    body += "Thank you!\n"

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(message["From"], message["To"], message.as_string())

    return "Verification email sent successfully."


def admin_disapproves_user(user_id: int)->bool:
    '''Admin disapproves user role'''
    sql='''UPDATE users SET is_approved = 0 WHERE (`id` = ?);'''
    data=update_query(sql,(user_id,))
    if data:
        return True
    return False

def view_admin(email: str = None, last_name: str = None)->list[User]:
    ''' Admin view all users'''
    sql='''SELECT id, email, password, first_name, last_name, role, phone_number, linked_in_account, verification_token, is_verified, is_approved 
           FROM users 
           LEFT JOIN teachers as t ON id=t.users_id'''
    where_clauses=[]
    if email:
        where_clauses.append(f"email like '%{email}%'")
    if last_name:
        where_clauses.append(f"last_name like '%{last_name}%'")
    
    if where_clauses:
        sql+= ' WHERE ' + ' AND '.join(where_clauses)

    data=read_query(sql, (id,))
    return (User.from_query_result_for_admin(*obj) for obj in data)

def approve_enrollment(student_id: int, course_id: int)-> bool:
    ''' Teacher approve student enrollement in his/her course'''
    if student_id is None or course_id is None:
        return None
    
    #status 0 = sub, 1 = enrolled, 2 = unsubscribed
    sql = "UPDATE users_have_courses SET status = ? WHERE users_id = ? AND courses_id = ?"
    sql_params = (1, student_id, course_id)
    if update_query(sql, sql_params):
        return True
    return False

def view_all_pending_approval_students(teacher_id: int)-> list[ViewUserCourse]:
    '''Teacher views all pending course enrollement for his/her course'''

    if teacher_id is None:
        return None

    sql = '''SELECT u.id, u.first_name, u.last_name, c.id, c.title
        FROM courses AS c
        JOIN users_have_courses AS uc ON c.id = uc.courses_id
        JOIN users AS u ON u.id = uc.users_id
        WHERE uc.status = 0 AND c.owner_id = ?'''

    sql_params = (teacher_id,)

    data = read_query(sql, sql_params)

    return [ViewUserCourse.from_query_result(*obj) for obj in data]


