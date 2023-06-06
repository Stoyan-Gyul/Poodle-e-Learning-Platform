
from data.database import read_query, insert_query, update_query
from data.common.models.course_response import CourseResponse
from data.common.models.course_update import CourseUpdate
from data.common.models.course import Course
from data.common.models.objective import Objective
from data.common.models.report import Report
from data.common.models.section import Section
from data.common.models.tag import Tag
from data.common.models.user_rating import UserRating
from data.common.models.user import User
from data.common.models.view_courses import ViewPublicCourse, ViewStudentCourse, ViewTeacherCourse, ViewAdminCourse
from data.common.constants import CourseStatus, CourseType
from fastapi import UploadFile
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def view_public_courses(rating: float = None,
                        tag: str  = None) -> list[ViewPublicCourse] :
    ''' View only title, description and tag of public course and search them by rating and tag'''

    sql='''SELECT c.id, c.title,  c.description, c.course_rating, t.expertise_area 
           FROM courses as c 
           JOIN courses_have_tags as ct 
           ON c.id=ct.courses_id 
           JOIN tags as t 
           ON t.id=ct.tags_id 
           WHERE is_premium = 0'''
    where_clauses=[]
    if rating:
        where_clauses.append(f"c.course_rating >= {rating}")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)
    
    return (ViewPublicCourse.from_query_result(*obj) for obj in read_query(sql))

def view_enrolled_courses(id: int, 
                          title: str = None,
                          tag: str  = None) -> list[ViewStudentCourse]:
    '''View public and enrolled courses of logged student and search them by title and tag'''

    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic, t.expertise_area, o.description, uc.progress 
           FROM courses AS c
           JOIN courses_have_tags AS ct ON c.id = ct.courses_id
           JOIN tags AS t ON t.id = ct.tags_id
		   JOIN courses_have_objectives as co ON c.id=co.courses_id
		   JOIN objectives as o ON o.id=co.objectives_id
           JOIN users_have_courses AS uc ON c.id = uc.courses_id
           WHERE c.is_active = 1 AND uc.status != 2 AND uc.users_id = ?'''
    
    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

    data=read_query(sql, (id,))

    courses = []
    for obj in data:
        course = ViewStudentCourse.from_query_result(*obj)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)

    return courses

def view_students_courses( user_id: int,  title: str = None,
                           tag: str  = None) -> list[ViewStudentCourse]:
    '''View all public and premium courses available for students and search them by title and tag'''

    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic, t.expertise_area, o.description as objectiv 
           FROM courses AS c
           JOIN courses_have_tags AS ct ON c.id = ct.courses_id
           JOIN tags AS t ON t.id = ct.tags_id
		   JOIN courses_have_objectives as co ON c.id=co.courses_id
		   JOIN objectives as o ON o.id=co.objectives_id
           LEFT JOIN `e-learning`.users_have_courses AS uhc ON c.id = uhc.courses_id AND uhc.users_id = ?
           WHERE c.is_active = 1 AND (uhc.users_id IS NULL OR uhc.status = 2)
           '''
    sql_params = (user_id,)

    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

    data=read_query(sql, sql_params)

    courses = []
    for obj in data:
        course = ViewStudentCourse.from_query_result(*obj)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)

    return courses

def view_teacher_courses(id: int, 
                          title: str = None,
                          tag: str  = None) -> list[ViewTeacherCourse]:
    '''View all public and premium courses of logged teacher and search them by title and tag'''
    
    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic, c.is_active, c.is_premium, t.expertise_area, o.description as objectiv 
           FROM courses AS c
           JOIN courses_have_tags AS ct ON c.id = ct.courses_id
           JOIN tags AS t ON t.id = ct.tags_id
		   JOIN courses_have_objectives as co ON c.id=co.courses_id
		   JOIN objectives as o ON o.id=co.objectives_id
           WHERE c.owner_id = ?'''
    
    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

    data=read_query(sql, (id,))

    courses = []
    for obj in data:
        course = ViewTeacherCourse.from_query_result(*obj)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)

    return courses

def course_rating(rating: int , course_id: int, student_id: int)-> bool:
    ''' Student can rate his enrolled course only one time'''
    try:
        sql='''SELECT rating 
            FROM users_have_courses 
            WHERE courses_id=? AND users_id=?'''
        data=read_query(sql, (course_id, student_id))
        if data[0][0]:
            return None # student can rate a course only once
        else:
            sql='''UPDATE users_have_courses 
                SET rating = ? 
                WHERE (users_id = ?) and (courses_id = ?)'''
                
            result=update_query(sql,(rating, student_id, course_id))
            if result:
                transaction=_course_rating_change_transaction(course_id)
                if transaction:
                    return True
                return None
    except:
        return None # student is not enrolled in this course


def get_all_reports(user_id: int):
    sql = '''SELECT u.users_id, u.courses_id, u.status, u.rating, u.progress
            FROM users_have_courses u
            JOIN courses c
            ON c.id = u.courses_id
            WHERE c.owner_id = ?'''
    sql_params = (user_id,)
    data = read_query(sql, sql_params)

    return (Report.from_query_result(*row) for row in data)


def get_reports_by_id(course_id: int):
    sql = '''
    SELECT uhc.users_id, uhc.courses_id, uhc.status, uhc.rating, uhc.progress, u.first_name, u.last_name, c.title
    FROM users_have_courses AS uhc
    JOIN users AS u ON u.id = uhc.users_id
    JOIN courses AS c ON c.id = uhc.courses_id
    WHERE uhc.courses_id = ?
    '''
    sql_params = (course_id,)
    data = read_query(sql, sql_params)
    return (Report.from_query_result(*row) for row in data)


def get_course_by_id(course_id: int)-> Course | None:
    ''' Get the course by id or return None if no such course exists'''
    sql = '''
            SELECT id, title, description, home_page_pic, owner_id, is_active, is_premium, course_rating
            FROM courses
            WHERE id = ?'''
    sql_params = (course_id,)
    data = read_query(sql, sql_params)

    course = next((Course.from_query_result(*row) for row in data), None)
    if course: 
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')

    return course


def get_tags(ids: list[int]) -> list[Tag]:
    ids_joined = ','.join(str(id) for id in ids)
    data = read_query(f'''
            SELECT id, expertise_area
            FROM tags 
            WHERE id IN ({ids_joined})''')

    return [Tag.from_query_result(*row) for row in data]


def get_course_tags(course_id: int) -> list[Tag]:
    data = read_query(
        '''SELECT t.id, t.expertise_area
                FROM tags t
                WHERE t.id in (SELECT tags_id
                                FROM courses_have_tags
                                WHERE courses_id = ?)''',
        (course_id,))

    return [Tag.from_query_result(*row) for row in data]


def get_objectives(ids: list[int]) -> list[Objective]:
    ids_joined = ','.join(str(id) for id in ids)
    data = read_query(f'''
            SELECT id, description
            FROM objectives 
            WHERE id IN ({ids_joined})''')

    return [Objective.from_query_result(*row) for row in data]


def get_course_objectives(course_id: int) -> list[Objective]:
    data = read_query(
        '''SELECT o.id, o.description
                FROM objectives o
                WHERE o.id in (SELECT objectives_id
                                FROM courses_have_objectives
                                WHERE courses_id = ?)''',
        (course_id,))

    return [Objective.from_query_result(*row) for row in data]


def insert_tags_in_course(course_id: int, tag_ids: list[int]):
    relations = ','.join(
        f'({course_id},{tag_id})' for tag_id in tag_ids)
    insert_query(
        f'INSERT INTO courses_have_tags(courses_id, tags_id) VALUES {relations}')


def insert_objectives_in_course(course_id: int, objective_ids: list[int]):
    relations = ','.join(
        f'({course_id},{objective_id})' for objective_id in objective_ids)
    insert_query(
        f'INSERT INTO courses_have_objectives(courses_id, objectives_id) VALUES {relations}')


def create_course(course: Course, owner: User):
    sql = '''INSERT into courses(title, description, home_page_pic, owner_id, is_active, is_premium)
            VALUES (?, ?, ?, ?, ?, ?)'''
    sql_params = (course.title, 
                  course.description, 
                  course.home_page_pic, 
                  owner.id, 
                  1 if course.is_active == CourseStatus.ACTIVE else 0, 
                  1 if course.is_premium == CourseType.PREMIUM else 0
                 )
    generated_id = insert_query(sql, sql_params)

    course.id = generated_id
    course.owner_id = owner.id

    insert_tags_in_course(course.id, course.tag_ids)
    insert_objectives_in_course(course.id, course.objective_ids)

    return course


def update_course(course_update: CourseUpdate, course: Course):
    sql = ('''
            UPDATE courses
            SET title = ?, 
                description = ?, 
                home_page_pic = ?, 
                is_active = ?, 
                is_premium = ?
            WHERE id = ?
            ''')
    sql_params = (course_update.title, 
                  course_update.description, 
                  course_update.home_page_pic, 
                  1 if course_update.is_active == 'active' else 0, 
                  1 if course_update.is_premium == 'premium' else 0, 
                  course.id
                  )
    result = update_query(sql, sql_params)

    if result > 0:
        course.title = course_update.title
        course.description = course_update.description
        course.home_page_pic = course_update.home_page_pic
        course.is_active = course_update.is_active
        course.is_premium = course_update.is_premium

    return course


def upload_pic(course_id: int, pic: UploadFile):

    if pic is None or course_id is None:
        return None

    sql = "UPDATE courses SET home_page_pic = ? WHERE id = ?"
    sql_p = (pic, course_id)
    return update_query(sql, sql_p)

def course_exists(id: int):
    return any(
        read_query(
            'SELECT * FROM courses WHERE id = ?',
            (id,)))


def get_section_by_id(section_id: int):
    data = read_query(
        '''SELECT id, title, content, description, external_link, courses_id
            FROM sections 
            WHERE id = ?''', (section_id,))
    
    return next((Section.from_query_result(*row) for row in data), None)


def get_course_sections(course_id: int):
    data = read_query(
        '''SELECT id, title, content, description, external_link, courses_id
            FROM sections 
            WHERE courses_id = ?''', (course_id,))

    return (Section.from_query_result(*row) for row in data)


def create_section(course_id: int, section: Section):
    sql = '''INSERT into sections(title, content, description, external_link, courses_id)
            VALUES (?, ?, ?, ?, ?)'''
    sql_params = section.title, section.content, section.description, section.external_link, course_id
    generated_id = insert_query(sql, sql_params)

    section.id = generated_id

    return section


def update_section(old: Section, new: Section):
    merged = Section(
        id=old.id,
        title=new.title or old.title,
        content=new.content or old.content,
        description=new.description or old.description,
        external_link=new.external_link or old.external_link,
        courses_id=new.courses_id or old.courses_id)

    update_query(
        '''UPDATE sections 
           SET title = ?, content = ?, description = ?, external_link = ?, courses_id = ?
           WHERE id = ? 
        ''',
        (merged.title, merged.content, merged.description, merged.external_link, merged.courses_id, merged.id))

    return merged


def view_admin_courses( title: str = None,
                           tag: str  = None,
                           teacher: str = None,
                           student: str  = None)-> list[ViewAdminCourse]:
    '''View all public and premium courses available for admin and search them by title and tag, teacher email and student email'''
    
    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic, c.is_active, c.is_premium, t.expertise_area, o.description as objectiv, uc.number_students
           FROM courses AS c
           JOIN courses_have_tags AS ct ON c.id = ct.courses_id
           JOIN tags AS t ON t.id = ct.tags_id
		   JOIN courses_have_objectives as co ON c.id=co.courses_id
		   JOIN objectives as o ON o.id=co.objectives_id
           JOIN (SELECT courses_id, count(courses_id) as number_students FROM users_have_courses GROUP BY courses_id) as uc ON c.id=uc.courses_id'''
    
    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    if teacher:
        sql+=' JOIN users as u ON c.owner_id=u.id'
        where_clauses.append(f"u.email like '%{teacher}%'")
    if student:
        sql+=''' JOIN users_have_courses as us ON us.courses_id=c.id
                 JOIN users as u1 ON us.users_id=u1.id'''
        where_clauses.append(f"u1.email like '%{student}%'")
    if where_clauses:
        sql+= ' WHERE ' + ' AND '.join(where_clauses)

    data=read_query(sql)
    courses = []
    for obj in data:
        course = ViewAdminCourse.from_query_result(*obj)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)

    return courses


def is_student_enrolled_in_course(course_id: int, student_id: int)->bool:
    '''Verify if student is enrolled in course'''

    return any(
        read_query(
            'SELECT * FROM users_have_courses WHERE courses_id=?  AND users_id=?',
            (course_id, student_id)))


def admin_removes_student_from_course(course_id: int,student_id: int)-> bool:
    ''' Admin removes student from course'''

    # sql='''DELETE FROM users_have_courses WHERE (courses_id = ?) and (users_id = ?)'''
    # if update_query(sql,(course_id, student_id)):
        #status 0 = sub, 1 = enrolled, 2 = unsubscribed
    sql = "UPDATE users_have_courses SET status = ? WHERE users_id = ? AND courses_id = ?"
    sql_params = (2, student_id, course_id)
    if update_query(sql, sql_params):
        return True
    return False


def has_course_section(course_id: int, section_id: int)->bool:
    ''' Verify if course has this section'''

    sql='''SELECT 1 FROM sections WHERE courses_id=? AND id=?'''
    return any(read_query(sql, (course_id,section_id)))


def view_section(course_id: int, section_id: int, user_id: int)->Section | None:
    '''View section by user AND increase the progress of student if for first time'''
    sql='''SELECT * FROM sections WHERE id=?'''
    data=read_query(sql, (section_id,))
    if is_section_viewed(section_id, user_id):
        return Section.from_query_result(*data[0])
    #increase the progess of student
    if validate_section(course_id, user_id, section_id):
        return Section.from_query_result(*data[0])
    

def is_section_viewed(section_id: int, user_id: int)-> bool:
    '''Verify if student viewed the section'''

    sql='''SELECT 1 FROM users_has_sections WHERE sections_id=? AND users_id=?'''
    return any(read_query(sql, (section_id, user_id)))


def validate_section(course_id: int, user_id:int, section_id: int)-> bool:
    ''' Increase student progress'''

    total_number_sections=number_sections_per_course(course_id)

    sql='''INSERT INTO users_has_sections (users_id, sections_id) VALUES (?, ?)'''
    if update_query(sql, (user_id, section_id)):
        viewed_sections=number_views_per_student(course_id, user_id)
        progress=round((viewed_sections/total_number_sections)*100, 0)
        # update course progress
        if update_query('''UPDATE users_have_courses 
                           SET progress = ? 
                           WHERE (`users_id` = ?) and (`courses_id` = ?)''', 
                        (progress, user_id, course_id)):
            return True
    return False


def number_sections_per_course(course_id: int)-> int:
    ''' Calculates the number of sections in the course'''

    sql='''SELECT count(id) FROM sections WHERE courses_id=?'''
    data=read_query(sql, (course_id,))
    return data[0][0]


def number_views_per_student(course_id: int, user_id: int)-> int:
    ''' Calculates the number sections view per course by student'''

    sql='''SELECT count(users_id) 
           FROM users_has_sections 
           WHERE users_id=? AND sections_id in (SELECT id FROM sections WHERE courses_id=?)'''
    data=read_query(sql, (user_id, course_id))
    return data[0][0]


def _course_rating_change_transaction(course_id: int)-> bool:
    ''' Calculate and change new course rating'''
    # calculates average course rating
    sql='SELECT rating FROM users_have_courses WHERE courses_id=?'

    data=read_query(sql,(course_id,))
    ratings=[]
    if data:
        for i in data:
            ratings.append(i[0])
        course_rating=round(sum(ratings)/len(ratings),1)

    # update course_rating in DB
        sql='''UPDATE courses 
            SET course_rating = ? WHERE (id = ?);'''
                
        result=update_query(sql,(course_rating, course_id))
        if result:
            return True
        else:
            return False # transaction not successful
    return False


def number_premium_courses_par_student(user_id: int)-> int:
    '''Get number of premium courses a student is enrolled in'''

    sql='''SELECT count(courses_id) 
           FROM users_have_courses 
           WHERE users_id=? AND courses_id in (SELECT id FROM courses WHERE is_premium=1)'''
    
    return read_query(sql, (user_id,))[0][0]


def is_course_premium(course_id: int)-> bool:
    '''Verify if course is premium'''

    sql='''SELECT 1 FROM courses WHERE is_premium=1 AND id=?'''
    return any(read_query(sql, (course_id,)))

def rating_history(course_id: int)-> list[UserRating] | None:
    '''Students ratings for a course or None if no enrolled'''

    sql='''SELECT u.email, uc.rating FROM users_have_courses as uc
           JOIN users as u on uc.users_id=u.id WHERE courses_id=?'''
    data=read_query(sql, (course_id,))
    if data:
        return (UserRating.from_query_result(*obj) for obj in data)
    return None

def is_course_active(course_id: int)-> bool:
    '''Verify if the course is active'''
    sql='''SELECT is_active FROM courses WHERE id=?'''
    data=read_query(sql, (course_id,))
    if data[0][0]: return True
    return False

def admin_removes_course(course_id: int)-> bool:
    '''Admin hide a course. Return True if status to non active change si non False'''
    # course status: active -1, hidden -0
    sql='''UPDATE courses SET is_active = 0 WHERE (id = ?)'''
    if update_query(sql, (course_id,)):
        if students_notification_by_email(course_id):
            return True
    return False

def students_notification_by_email(course_id: int)-> bool:
    '''Notification of students enrolled in hidden course'''
    sql='''SELECT u.email, u.first_name, u.last_name, c.title FROM users_have_courses as uc
           JOIN users as u on uc.users_id=u.id 
           JOIN courses as c ON uc.courses_id=c.id WHERE uc.courses_id=?'''
    data=read_query(sql, (course_id,))
    for obj in data:
        try:
            send_email_to_student_for_hidden_course(obj[0],obj[1],obj[2],obj[3])
        except:
            return False
        return True

def send_email_to_student_for_hidden_course(student_email: int, student_first_name: str, student_last_name: str, course_title: str)-> bool:
    '''Send email to student that the course is not more available'''
    smtp_host = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "poodle.learning@outlook.com"
    smtp_password = "1234@alpha"  # Use your Outlook.com account password

    message = MIMEMultipart()
    message["From"] = "poodle.learning@outlook.com"
    message["To"] = student_email
    message["Subject"] = "Hidden course notification"

    body = f"Dear {student_first_name} {student_last_name},\n\n"
    body += f"We would like to inform you that class '{course_title}' has been removed.\n"
    body += f"You cannot see this course anymore.\n\n"
    body += "Thank you for your understanding!\n"

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(message["From"], message["To"], message.as_string())

        return True


def create_response_object(course: Course, tags: list[Tag], objectives: list[Objective], sections: list[Section]):
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        home_page_pic=course.home_page_pic,
        owner_id=course.owner_id,
        is_active=course.is_active,
        is_premium=course.is_premium,
        rating=course.rating,
        tags=tags,
        objectives=objectives,
        sections=sections
    )
