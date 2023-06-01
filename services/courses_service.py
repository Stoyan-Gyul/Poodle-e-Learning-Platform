
from data.database import read_query, insert_query, update_query
from data.models import Report, Course, Section, CourseUpdate
from data.models import ViewPublicCourse, ViewStudentCourse, ViewTeacherCourse, ViewAdminCourse
from fastapi import UploadFile
import base64

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


def view_students_courses( title: str = None,
                           tag: str  = None) -> list[ViewStudentCourse]:
    '''View all public and premium courses available for students and search them by title and tag'''

    sql='''SELECT c.id, c.title, c.description, c.course_rating, c.home_page_pic, t.expertise_area, o.description as objectiv 
           FROM courses AS c
           JOIN courses_have_tags AS ct ON c.id = ct.courses_id
           JOIN tags AS t ON t.id = ct.tags_id
		   JOIN courses_have_objectives as co ON c.id=co.courses_id
		   JOIN objectives as o ON o.id=co.objectives_id
           WHERE c.is_active = 1'''
    
    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

    data=read_query(sql)

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
    sql = '''SELECT users_id, courses_id, status, rating, progress 
            FROM users_have_courses 
            WHERE courses_id = ?'''
    sql_params = (course_id,)
    data = read_query(sql, sql_params)

    return (Report.from_query_result(*row) for row in data)


def get_course_by_id(course_id: int):
    sql = '''
            SELECT c.id, c.title, c.description, c.home_page_pic, c.owner_id, c.is_active, c.is_premium, t.expertise_area, o.description
            FROM courses AS c
            JOIN courses_have_tags AS ct ON c.id = ct.courses_id
            JOIN tags AS t ON t.id = ct.tags_id
            JOIN courses_have_objectives as co ON c.id = co.courses_id
            JOIN objectives as o ON o.id = co.objectives_id
            WHERE c.id = ?'''
    sql_params = (course_id,)
    data = read_query(sql, sql_params)

    if data is None:
        return None
    else:
        course = Course.from_query_result(id=data[0][0], title=data[0][1], description=data[0][2], home_page_pic=data[0][3], owner_id=data[0][4], is_active=data[0][5], is_premium=data[0][6], expertise_area=data[0][7], objective=data[0][8])
        if course.home_page_pic is not None:
            course.home_page_pic = base64.b64encode(course.home_page_pic).decode('utf-8')

        return course


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


def get_sections_by_course(course_id: int):
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
                           tag: str  = None)-> list[ViewAdminCourse]:
    '''View all public and premium courses available for admin and search them by title and tag'''
    
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
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

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