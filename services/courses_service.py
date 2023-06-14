
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

    sql='''SELECT c.id, c.title,  c.description, c.course_rating
           FROM courses as c
           WHERE c.is_premium = 0 and c.is_active = 1'''
    courses_data=read_query(sql, (id,))
    courses = []
    for c in courses_data:
        course_id = c[0]

        sql_tags_list = '''
            SELECT t.expertise_area
            FROM courses_have_tags AS ct
            JOIN tags AS t ON t.id = ct.tags_id
            WHERE ct.courses_id = ?
        '''
            
        sql_tags_params = (course_id,)
        tags_data = read_query(sql_tags_list, sql_tags_params)
        tags_data = [tag[0] for tag in tags_data]  # Flatten the list of tags

        course = ViewPublicCourse.from_query_result(id=c[0], title=c[1], description=c[2], course_rating=c[3],
                                                     tags=tags_data)
        courses.append(course)
    
    return courses
    
def view_enrolled_courses(id: int, 
                          title: str = None,
                          tag: str  = None) -> list[ViewStudentCourse]:
    '''View enrolled courses of a logged student and search them by title and tag'''

    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic
           FROM courses AS c
           JOIN users_have_courses AS uc ON c.id = uc.courses_id
           WHERE c.is_active = 1 AND uc.status = 1 AND uc.users_id = ?'''
    

    courses_data=read_query(sql, (id,))
    courses = []
    for c in courses_data:
        course_id = c[0]

        sql_tags_list = '''
            SELECT t.expertise_area
            FROM courses_have_tags AS ct
            JOIN tags AS t ON t.id = ct.tags_id
            WHERE ct.courses_id = ?
        '''
            
        sql_tags_params = (course_id,)
        tags_data = read_query(sql_tags_list, sql_tags_params)
        tags_data = [tag[0] for tag in tags_data]  # Flatten the list of tags

        sql_obj_list = '''
            SELECT o.description
            FROM courses_have_objectives AS co
            JOIN objectives AS o ON o.id = co.objectives_id
            WHERE co.courses_id = ?
        '''
            
        sql_obj_params = (course_id,)
        obj_data = read_query(sql_obj_list, sql_obj_params)
        obj_data = [objective[0] for objective in obj_data]  # Flatten the list of objectives

        course = ViewStudentCourse.from_query_result(id=c[0], title=c[1], description=c[2], course_rating=c[3],
                                                     home_page_pic=c[4], tags=tags_data, objectives=obj_data)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)
    
    return courses

    # where_clauses=[]
    # if title:
    #     where_clauses.append(f"c.title like '%{title}%'")
    # if tag:
    #     where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    # if where_clauses:
    #     sql+= ' AND ' + ' AND '.join(where_clauses)

def view_students_courses(user_id: int, title: str = None, tag: str = None) -> list[ViewStudentCourse]:
    '''View all public and premium courses available for students and search them by title and tag'''

    sql = '''
        SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic
        FROM courses AS c
        LEFT JOIN users_have_courses AS uhc ON c.id = uhc.courses_id AND uhc.users_id = ?
        WHERE c.is_active = 1 AND (uhc.users_id IS NULL OR uhc.status = 2)
    '''
    
    courses_data = read_query(sql, (user_id,))

    courses = []
    for c in courses_data:
        course_id = c[0]

        sql_tags_list = '''
            SELECT t.expertise_area
            FROM courses_have_tags AS ct
            JOIN tags AS t ON t.id = ct.tags_id
            WHERE ct.courses_id = ?
        '''
            
        sql_tags_params = (course_id,)
        tags_data = read_query(sql_tags_list, sql_tags_params)
        tags_data = [tag[0] for tag in tags_data]  # Flatten the list of tags

        sql_obj_list = '''
            SELECT o.description
            FROM courses_have_objectives AS co
            JOIN objectives AS o ON o.id = co.objectives_id
            WHERE co.courses_id = ?
        '''
            
        sql_obj_params = (course_id,)
        obj_data = read_query(sql_obj_list, sql_obj_params)
        obj_data = [objective[0] for objective in obj_data]  # Flatten the list of objectives

        course = ViewStudentCourse.from_query_result(id=c[0], title=c[1], description=c[2], course_rating=c[3],
                                                     home_page_pic=c[4], tags=tags_data, objectives=obj_data)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)
    
    return courses

def view_teacher_courses(id: int, title: str = None, tag: str = None) -> list[ViewTeacherCourse]:
    '''View all public and premium courses of logged teacher and search them by title and tag'''

    sql = '''
        SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic, c.is_active, c.is_premium
        FROM courses AS c
        WHERE c.owner_id = ?
    '''

    course_data = read_query(sql, (id,))

    courses = []
    for c in course_data:
        course_id = c[0]

        sql_tags_list = '''
            SELECT t.expertise_area
            FROM courses AS c
            JOIN courses_have_tags AS ct ON c.id = ct.courses_id
            JOIN tags AS t ON t.id = ct.tags_id
            WHERE c.owner_id = ? AND c.id = ?
        '''

        sql_tags_params = (id, course_id)
        tags_data = read_query(sql_tags_list, sql_tags_params)
        tags_data = [tag[0] for tag in tags_data]  # Flatten the list of tags

        sql_obj_list = '''
            SELECT o.description
            FROM courses AS c
            JOIN courses_have_objectives AS co ON c.id = co.courses_id
            JOIN objectives AS o ON o.id = co.objectives_id
            WHERE c.owner_id = ? AND c.id = ?
        '''

        sql_obj_params = (id, course_id)
        obj_data = read_query(sql_obj_list, sql_obj_params)
        obj_data = [objective[0] for objective in obj_data]  # Flatten the list of objectives

        course = ViewTeacherCourse.from_query_result(id=c[0], title=c[1], description=c[2], course_rating=c[3],
                                                     home_page_pic=c[4], is_active=c[5], is_premium=c[6],
                                                     tags=tags_data, objectives=obj_data)
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
            SELECT c.id, c.title, c.description, c.home_page_pic, c.course_rating, c.owner_id, c.is_active, c.is_premium
            FROM courses AS c
            WHERE c.id = ?'''
    sql_params = (course_id,)
    data = read_query(sql, sql_params)

    if not data:
        return None
    else:

        sql_tags_list = '''
            SELECT t.expertise_area
            FROM courses_have_tags AS ct
            JOIN tags AS t ON t.id = ct.tags_id
            WHERE courses_id = ?
        '''

        sql_tags_params = (course_id,)
        tags_data = read_query(sql_tags_list, sql_tags_params)
        tags_data = [tag[0] for tag in tags_data]  # Flatten the list of tags

        sql_obj_list = '''
            SELECT o.description
            FROM courses_have_objectives AS co
            JOIN objectives AS o ON o.id = co.objectives_id
            WHERE courses_id = ?
        '''

        sql_obj_params = (course_id,)
        obj_data = read_query(sql_obj_list, sql_obj_params)
        obj_data = [objective[0] for objective in obj_data]  # Flatten the list of objectives

        course = Course.from_query_result(id=data[0][0], title=data[0][1], description=data[0][2], home_page_pic = data[0][3], course_rating=data[0][4],
                                                    owner_id=data[0][5], is_active=data[0][6], is_premium=data[0][7],
                                                    tags=tags_data, objectives=obj_data)
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

def tag_exists(tag):
    sql = "SELECT id FROM tags WHERE expertise_area = ?"
    sql_params = (tag,)

    result = read_query(sql, sql_params)

    if result:
        return result[0]
    else:
        return None

def create_new_tag(tag: str):
    sql = "INSERT INTO tags (expertise_area) VALUES (?)"
    sql_params = (tag,)

    return insert_query(sql, sql_params) # Return the newly created tag_id

def create_course_tag(course_id: int, tag_id: int):
    sql = '''INSERT INTO courses_have_tags(courses_id, tags_id) VALUES (?, ?)'''
    sql_params = (course_id, tag_id)

    return insert_query(sql, sql_params)   

def insert_tags_in_course(course_id: int, tags: list[str]):
    
    for tag in tags:
        if tag_exists(tag):
            tag_id = tag_exists(tag)[0]
            create_course_tag(course_id, tag_id)
        else:
            newly_create_tag_id = create_new_tag(tag)
            create_course_tag(course_id, newly_create_tag_id)

def objective_exists(objective):
    sql = "SELECT id FROM objectives WHERE description = ?"
    sql_params = (objective,)

    result = read_query(sql, sql_params)

    if result:
        return result[0]  # Return the objecive_id if objective exists
    else:
        return None

def create_new_objective(objective: str):
    sql = "INSERT INTO objectives (description) VALUES (?)"
    sql_params = (objective,)

    return insert_query(sql, sql_params) # Return the newly created objective_id

def create_course_objective(course_id: int, objective_id: int):
    sql = "INSERT INTO courses_have_objectives (courses_id, objectives_id) VALUES (?, ?)"
    sql_params = (course_id, objective_id)

    return insert_query(sql, sql_params)   

def insert_objectives_in_course(course_id: int, objectives: list[str]):

    for obj in objectives:

        if objective_exists(obj):
            obj_id = objective_exists(obj)[0]
            create_course_objective(course_id, obj_id)
        else:
            newly_create_obj_id = create_new_objective(obj)
            create_course_objective(course_id, newly_create_obj_id)

def create_course(course: Course):
    sql = '''INSERT into courses(title, description, home_page_pic, owner_id, is_active, is_premium)
            VALUES (?, ?, ?, ?, ?, ?)'''
    sql_params = (course.title, 
                  course.description, 
                  course.home_page_pic, 
                  course.owner_id,
                  1 if course.is_active == 'active' else 0, 
                  1 if course.is_premium == 'premium' else 0
                 )
    generated_id = insert_query(sql, sql_params)

    course.id = generated_id


    insert_tags_in_course(course.id, course.tags)
    insert_objectives_in_course(course.id, course.objectives)

    return course

def update_course(course_update: CourseUpdate, course: Course):
    sql = ('''
            UPDATE courses
            SET title = ?, 
                description = ?,  
                is_active = ?, 
                is_premium = ?
            WHERE id = ?
            ''')
    sql_params = (course_update.title, 
                  course_update.description,  
                  1 if course_update.is_active == 'active' else 0, 
                  1 if course_update.is_premium == 'premium' else 0, 
                  course.id
                  )
    result = update_query(sql, sql_params)

    if result > 0:
        course.title = course_update.title
        course.description = course_update.description
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
    
def view_all_sections_for_a_course(course_id: int):
    sql = '''SELECT * FROM sections WHERE courses_id=?'''
    sql_params = (course_id,)
    data=read_query(sql, sql_params)

    return [Section.from_query_result(*obj) for obj in data]

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


def view_student_pending_approval_by_teacher_courses(student_id: int):

    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic
           FROM courses AS c
           JOIN users_have_courses AS uc ON c.id = uc.courses_id
           WHERE c.is_active = 1 AND uc.status = 0 AND uc.users_id = ?'''
    

    courses_data=read_query(sql, (student_id,))
    courses = []
    for c in courses_data:
        course_id = c[0]

        sql_tags_list = '''
            SELECT t.expertise_area
            FROM courses_have_tags AS ct
            JOIN tags AS t ON t.id = ct.tags_id
            WHERE ct.courses_id = ?
        '''
            
        sql_tags_params = (course_id,)
        tags_data = read_query(sql_tags_list, sql_tags_params)
        tags_data = [tag[0] for tag in tags_data]  # Flatten the list of tags

        sql_obj_list = '''
            SELECT o.description
            FROM courses_have_objectives AS co
            JOIN objectives AS o ON o.id = co.objectives_id
            WHERE co.courses_id = ?
        '''
            
        sql_obj_params = (course_id,)
        obj_data = read_query(sql_obj_list, sql_obj_params)
        obj_data = [objective[0] for objective in obj_data]  # Flatten the list of objectives

        course = ViewStudentCourse.from_query_result(id=c[0], title=c[1], description=c[2], course_rating=c[3],
                                                     home_page_pic=c[4], tags=tags_data, objectives=obj_data)
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')
        courses.append(course)
    
    return courses