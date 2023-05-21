from data.database import read_query
from data.models import ViewPublicCourse, ViewStudentCourse

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

def view_public_and_enrolled_courses(id: int, 
                                     title: str = None,
                                     tag: str  = None):
    '''View public and enrolled courses of student and search them by title and tag'''
    
    sql='''SELECT c.title, c.description, c.home_page_pic, t.expertise_area 
           FROM courses as c 
           JOIN courses_have_tags as ct 
           ON c.id=ct.courses_id 
           JOIN tags as t 
           ON t.id=ct.tags_id 
           JOIN users_have_courses as uc 
           ON c.id = uc.courses_id 
           WHERE c.is_active=1 AND uc.users_id=?'''
    
    where_clauses=[]
    if title:
        where_clauses.append(f"c.title like '%{title}%'")
    if tag:
        where_clauses.append(f"t.expertise_area like '%{tag}%'")
    
    if where_clauses:
        sql+= ' AND ' + ' AND '.join(where_clauses)

    data=read_query(sql, (id,))
    return (ViewStudentCourse.from_query_result(*obj) for obj in data)