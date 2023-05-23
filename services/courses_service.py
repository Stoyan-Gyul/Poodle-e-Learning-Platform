from data.database import read_query, update_query
from data.models import ViewPublicCourse, ViewStudentCourse, ViewTeacherCourse

def view_public_courses() -> list[ViewPublicCourse] :
    ''' View only title, description and tag of public course'''

    sql='''SELECT c.title, c.description, t.expertise_area 
           FROM courses as c 
           JOIN courses_have_tags as ct 
           ON c.id=ct.courses_id 
           JOIN tags as t 
           ON t.id=ct.tags_id 
           WHERE is_premium = 0'''
    
    return (ViewPublicCourse.from_query_result(*obj) for obj in read_query(sql))

def view_enrolled_courses(id: int, 
                          title: str = None,
                          tag: str  = None) -> list[ViewStudentCourse]:
    '''View public and enrolled courses of logged student and search them by title and tag'''

    sql='''SELECT c.id, c.title, c.description, c.home_page_pic, t.expertise_area, o.description as objectiv 
           FROM courses AS c
           JOIN courses_have_tags AS ct ON c.id = ct.courses_id
           JOIN tags AS t ON t.id = ct.tags_id
		   JOIN courses_have_objectives as co ON c.id=co.courses_id
		   JOIN objectives as o ON o.id=co.objectives_id
           JOIN users_have_courses AS uc ON c.id = uc.courses_id
           WHERE c.is_active = 1 AND uc.users_id = ?'''
    
    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

    data=read_query(sql, (id,))
    return (ViewStudentCourse.from_query_result(*obj) for obj in data)


def view_students_courses( title: str = None,
                           tag: str  = None) -> list[ViewStudentCourse]:
    '''View all public and premium courses available for students and search them by title and tag'''

    sql='''SELECT c.id, c.title, c.description, c.home_page_pic, t.expertise_area, o.description as objectiv 
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
    return (ViewStudentCourse.from_query_result(*obj) for obj in data)


def view_teacher_course(id: int, 
                          title: str = None,
                          tag: str  = None) -> list[ViewTeacherCourse]:
    '''View all public and premium courses of logged teacher and search them by title and tag'''
    
    sql='''SELECT c.id, c.title, c.description, c.home_page_pic, c.is_active, c.is_premium, t.expertise_area, o.description as objectiv 
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
    return (ViewTeacherCourse.from_query_result(*obj) for obj in data)


def course_rating(rating: float , course_id: int, student_id: int)-> bool:
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
            if result>0:
                return True
    except:
        return None # student is not enrolled in this course