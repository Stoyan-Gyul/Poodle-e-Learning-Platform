from unittest import TestCase
from services import courses_service
from unittest import mock
from unittest.mock import MagicMock, patch, ANY
from data.models import ViewPublicCourse, ViewStudentCourse, ViewTeacherCourse
class CoursesService_Should(TestCase):
    
    @patch('services.courses_service.read_query', autospec=True)
    def test_view_public_courses_return_list_public_courses(self, mock_read_query):
        mock_read_query.return_value=[('Core Python', 'This is core modul', 'software developement'), ('General Python', 'This is general', 'software developement')]
        result=list(courses_service.view_public_courses())
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0],ViewPublicCourse)


    @patch('services.courses_service.read_query', autospec=True)
    def test_view_enrolled_courses_return_list_enrolled_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul', None, 'software developement', 'Learn software'),
                                      (2, 'OOP', 'This is OOP modul', None, 'software developement', 'Learn software')]
        result=list(courses_service.view_enrolled_courses(2))
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0],ViewStudentCourse)


    @patch('services.courses_service.read_query', autospec=True)
    def test_view_students_courses_return_list_public_and_premium_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul', None, 'software developement', 'Learn software'),
                                      (2, 'OOP', 'This is OOP modul', None, 'software developement', 'Learn software'),
                                      (4, 'General Python', 'This is general', None, 'software developement', 'General view')]
        result=list(courses_service.view_students_courses())
        self.assertEqual(3, len(result))
        self.assertIsInstance(result[0],ViewStudentCourse)

    @patch('services.courses_service.read_query', autospec=True)
    def test_view_teacher_course_return_list_owned_public_and_premium_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul', None, 1, 0, 'software developement', 'Learn software'),
                                      (2, 'OOP', 'This is OOP modul', None, 1, 1, 'software developement', 'Learn software'),
                                      (4, 'General Python', 'This is general', None, 1, 0, 'software developement', 'General view')]
        result=list(courses_service.view_teacher_course(1))
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
            result=courses_service.course_rating(6.0,2,2)
        self.assertEqual(True, result)

    @patch('services.courses_service.read_query', autospec=True)
    def test_course_rating_return_None_when_student_rates_course_not_enrolled_in(self, mock_read_query):
        mock_read_query.return_value=[(None,)]
        with patch('services.courses_service.update_query') as mock_update_query:
            mock_update_query.return_value=-1
            result=courses_service.course_rating(6.0,2,2)
        self.assertIsNone(result)

    
