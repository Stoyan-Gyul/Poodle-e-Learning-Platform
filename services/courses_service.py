from data.database import read_query
from data.models import ViewPublicCourse

def view_public_courses() -> list :
    sql='''SELECT c.title, c.description, t.expertise_area 
           FROM courses as c 
           JOIN courses_have_tags as ct 
           ON c.id=ct.courses_id 
           JOIN tags as t 
           ON t.id=ct.tags_id 
           WHERE is_premium = 0'''
    
    return (ViewPublicCourse.from_query_result(*obj) for obj in read_query(sql))