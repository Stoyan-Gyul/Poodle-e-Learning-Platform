from unittest import TestCase
from services import courses_service
from unittest import mock
from unittest.mock import MagicMock, patch, ANY
from data.models import ViewPublicCourse, ViewStudentCourse, ViewTeacherCourse, Report, Course, CourseUpdate, Section
class CoursesService_Should(TestCase):
    
    @patch('services.courses_service.read_query', autospec=True)
    def test_view_public_courses_return_list_public_courses(self, mock_read_query):
        mock_read_query.return_value=[('Core Python', 'This is core modul',8.0, 'software developement'), ('General Python', 'This is general',7.0, 'software developement')]
        result=list(courses_service.view_public_courses())
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0],ViewPublicCourse)


    @patch('services.courses_service.read_query', autospec=True)
    def test_view_enrolled_courses_return_list_enrolled_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul',8.0, None, 'software developement', 'Learn software'),
                                      (2, 'OOP', 'This is OOP modul',8.0, None, 'software developement', 'Learn software')]
        result=list(courses_service.view_enrolled_courses(2))
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0],ViewStudentCourse)


    @patch('services.courses_service.read_query', autospec=True)
    def test_view_students_courses_return_list_public_and_premium_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul',8.0, None, 'software developement', 'Learn software'),
                                      (2, 'OOP', 'This is OOP modul',8.0, None, 'software developement', 'Learn software'),
                                      (4, 'General Python', 'This is general',8.0, None, 'software developement', 'General view')]
        result=list(courses_service.view_students_courses())
        self.assertEqual(3, len(result))
        self.assertIsInstance(result[0],ViewStudentCourse)

    @patch('services.courses_service.read_query', autospec=True)
    def test_view_teacher_course_return_list_owned_public_and_premium_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul',8.0, None, 1, 0, 'software developement', 'Learn software'),
                                      (2, 'OOP', 'This is OOP modul',8.0, None, 1, 1, 'software developement', 'Learn software'),
                                      (4, 'General Python', 'This is general',8.0, None, 1, 0, 'software developement', 'General view')]
        result=list(courses_service.view_teacher_courses(1))
        self.assertEqual(3, len(result))
        self.assertIsInstance(result[0],ViewTeacherCourse)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_rating_return_None_when_student_rates_for_second_time(self, mock_read_query):
        mock_read_query.return_value=[(1,)]
        result=courses_service.course_rating(6.0,2,2)
        self.assertIsNone(result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_rating_return_True_when_student_rates_his_course_for_first_time(self, mock_read_query):
        mock_read_query.return_value=[(None,)]
        with patch('services.courses_service.update_query') as mock_update_query:
            mock_update_query.return_value=1
            with patch('services.courses_service._course_rating_change_transaction') as mock_trans:
                mock_trans.return_value=True
                result=courses_service.course_rating(6.0,2,2)
        self.assertEqual(True, result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_rating_return_None_when_student_rates_course_not_enrolled_in(self, mock_read_query):
        mock_read_query.return_value=[(None,)]
        with patch('services.courses_service.update_query') as mock_update_query:
            mock_update_query.return_value=-1
            result=courses_service.course_rating(6.0,2,2)
        self.assertIsNone(result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_all_reports(self,mock_read_query):
        mock_read_query.return_value=[(2, 1, 0, 6.0, None),
                                      (2, 2, 0, 6.0, None), 
                                      (3, 2, 0, 7.0, None),
                                      (3, 4, 0, 7.0, None)]
        
        result=list(courses_service.get_all_reports(1))
        self.assertIsInstance(result[0], Report)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_reports_by_id(self, mock_read_query):
        mock_read_query.return_value=[(2, 1, 0, 6.0, None)]

        result=list(courses_service.get_reports_by_id(1))
        self.assertIsInstance(result[0], Report)


    @patch('services.courses_service.read_query', autospec=True)
    def test_get_course_by_id_returnCourse_ifExists(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul', None, 1, 1, 0, 'software developement', 'Learn software')]
        result=courses_service.get_course_by_id(1)
        self.assertIsInstance(result, Course)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_course_by_id_returnNone_ifNoExist(self, mock_read_query):
        mock_read_query.return_value=[]
        result=courses_service.get_course_by_id(100)
        self.assertIsNone(result)

    @patch('services.courses_service.insert_query', autospec=True)
    def test_create_course_return_Course(self, mock_insert_query):
        mock_insert_query.return_value=1
        course=Course(title='fake_title',
                      description='any',
                      owner_id=1,
                      home_page_pic=None,
                      is_active='active',
                      is_premium='public')
        
        result=courses_service.create_course(course)

        self.assertIsInstance(result, Course)

    @patch('services.courses_service.update_query', autospec=True)
    def test_update_course_return_Course(self, mock_update_query):
        mock_update_query.return_value=True
        course=Course(title='fake_title',
                      description='any',
                      owner_id=1,
                      home_page_pic=None,
                      is_active='active',
                      is_premium='public')
        course_update=CourseUpdate(title='fake_title1',
                      description='Test',
                      home_page_pic=None,
                      is_active='hidden',
                      is_premium='premium')
        result=courses_service.update_course(course_update,course)
        self.assertIsInstance(result, Course)
        self.assertEqual('fake_title1', result.title)
        self.assertEqual('Test', result.description)
        self.assertEqual(None, result.home_page_pic)
        self.assertEqual('hidden', result.is_active)
        self.assertEqual('premium', result.is_premium)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_exists_returnTrue_ifExists(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul', None, 1, 1, 0)]

        result=courses_service.course_exists(1)
        self.assertEqual(True, result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_exists_returnFalse_ifNoExist(self, mock_read_query):
        mock_read_query.return_value=[]

        result=courses_service.course_exists(1)
        self.assertEqual(False, result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_section_by_id_returnSection_ifExists(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Basics',
                                          'Lorem ipsum dolor',
                                          'Explain the basics',
                                          'ext_link', 1)]
        result=courses_service.get_section_by_id(1)
        self.assertIsInstance(result, Section)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_section_by_id_returnNone_ifNoExist(self, mock_read_query):
        mock_read_query.return_value=[]
        result=courses_service.get_section_by_id(100)
        self.assertIsNone(result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_section_by_course_returnlistOfSections_ifCourseExist(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Basics',
                                        'Lorem ipsum dolor',
                                        'Explain the basics',
                                        'ext_link', 1),
                                        (2, 'Basics2',
                                        'Lorem ipsum dolor',
                                        'Explain the basics2',
                                        'ext_link2', 1)]
        result=list(courses_service.get_sections_by_course(1))
        self.assertIsInstance(result[0], Section)
        self.assertEqual(2, len(result))

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_section_by_course_returnEmptylistOfSections_ifNoCourse(self, mock_read_query):
        mock_read_query.return_value=[]
        result=list(courses_service.get_sections_by_course(100))
        
        self.assertEqual(0, len(result))

    @patch('services.courses_service.insert_query', autospec=True)
    def test_create_section(self, mock_insert_query):
        mock_insert_query.return_value=10
        section=Section(title='title1',
                        content='content1',
                        description='desc1',
                        external_link='extlink',
                        courses_id=1)

        result=courses_service.create_section(1,section)
        self.assertIsInstance(result, Section)


    @patch('services.courses_service.update_query', autospec=True)
    def test_update_section(self, mock_update_query):
        mock_update_query.return_value=True
        old=Section(id=1,
                    title='title1',
                    content='content1',
                    description='desc1',
                    external_link='extlink',
                    courses_id=1)
        new=Section(title='title2',
                    content='content2',
                    description='desc2',
                    external_link='extlink2',
                    courses_id=2)
        result=courses_service.update_section(old,new)
        self.assertIsInstance(result, Section)
        self.assertEqual('title2', result.title)
        self.assertEqual('content2', result.content)
        self.assertEqual('desc2', result.description)
        self.assertEqual('extlink2', result.external_link)
        self.assertEqual(2, result.courses_id)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_rating_change_transaction_return_True_when_trunsactionSuccessful(self, mock_read_query):
        mock_read_query.return_value=[(6,),(7,)]
        
        with patch('services.courses_service.update_query') as mock_update_query:
            mock_update_query.return_value=True
            result=courses_service._course_rating_change_transaction(2)
            self.assertEqual(True, result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_rating_change_transaction_return_False_when_NoRating(self, mock_read_query):
        mock_read_query.return_value=[]

        with patch('services.courses_service.update_query') as mock_update_query:
            mock_update_query.return_value=True
            result=courses_service._course_rating_change_transaction(2)
            self.assertEqual(False, result)



    
    

    






    

