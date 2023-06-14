from unittest import TestCase
from services import courses_service
from unittest import mock
from unittest.mock import MagicMock, patch, ANY, call
from data.common.models.view_courses import ViewPublicCourse, ViewStudentCourse, ViewTeacherCourse
from data.common.models.report import Report
from data.common.models.course import Course
from data.common.models.course_update import CourseUpdate
from data.common.models.section import Section
class CoursesService_Should(TestCase):
    
    @patch('services.courses_service.read_query', autospec=True)
    def test_view_public_courses_return_list_public_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core python description',8.0, ['python', 'core']), 
                                      (2, 'General Python', 'This is general python description ',7.0, ['python', 'general'])]
        result=list(courses_service.view_public_courses())
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0],ViewPublicCourse)
        self.assertIsInstance(result[1],ViewPublicCourse)

    @patch('services.courses_service.read_query', autospec=True)
    def test_view_enrolled_courses_return_list_enrolled_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul',8.0, None, ['python', 'core'], ['obj 1', 'obj 2'], 7.5),
                                      (2, 'OOP', 'This is OOP modul',8.0, None, ['python', 'oop'], ['obj 3', 'obj 4'], 10)]
        result=list(courses_service.view_enrolled_courses(2))
        self.assertEqual(2, len(result))
        self.assertIsInstance(result[0],ViewStudentCourse)
        self.assertIsInstance(result[1],ViewStudentCourse)

    @patch('services.courses_service.read_query', autospec=True)
    def test_view_students_courses_return_list_public_and_premium_courses(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Core Python', 'This is core modul',8.0, None, ['python', 'core'], ['obj 1', 'obj 2'], 7.5),
                                      (2, 'OOP', 'This is OOP modul',8.0, None, ['python', 'oop'], ['obj 3', 'obj 4'], 10 ),
                                      (3, 'General Python', 'This is general',8.0, None, ['python', 'general'], ['obj 5', 'obj 6'], 10 )]
        user_id = 1
        result=list(courses_service.view_students_courses(user_id))
        self.assertEqual(3, len(result))
        self.assertIsInstance(result[0],ViewStudentCourse)
        self.assertIsInstance(result[1],ViewStudentCourse)
        self.assertIsInstance(result[2],ViewStudentCourse)

    @patch('services.courses_service.read_query', autospec=True)
    def test_view_teacher_course_return_list_owned_public_and_premium_courses(self, mock_read_query):
        mock_read_query.side_effect = [
        [
            (1, 'Core Python', 'This is core module', 8.0, None, 'active', 'public'),
            (2, 'OOP', 'This is OOP module', 8.0, None, 'active', 'premium'),
            (3, 'General Python', 'This is general', 8.0, None, 'hidden', 'public')
        ],
        
        [('python',), ('core',)],
        [('obj 1',), ('obj 2',)],
       
        [('python',), ('oop',)],
        [('obj 3',), ('obj 4',)],
        
        [('python',), ('general',)],
        [('obj 5',), ('obj 6',)]
    ]
        teacher_id = 1
        result = courses_service.view_teacher_courses(teacher_id)
    
        expected_results = [
        ViewTeacherCourse.from_query_result(
            id=1, title='Core Python', description='This is core module', course_rating=8.0, home_page_pic=None, is_active='active', is_premium='public', tags=['python', 'core'], objectives=['obj 1', 'obj 2']),
        ViewTeacherCourse.from_query_result(
            id=2, title='OOP', description='This is OOP module', course_rating=8.0, home_page_pic=None, is_active='active', is_premium='premium', tags=['python', 'oop'], objectives=['obj 3', 'obj 4']),
        ViewTeacherCourse.from_query_result(
            id=3, title='General Python', description='This is general', course_rating=8.0,home_page_pic=None, is_active='hidden', is_premium='public', tags=['python', 'general'], objectives=['obj 5', 'obj 6'])
    ]
        self.assertEqual(len(result), 3)
        self.assertEqual(result, expected_results)

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
        mock_read_query.return_value=[(2, 1, 0, 6.0, 25, 'first_name 1', 'last_name 1', 'test course 1'),
                                      (2, 2, 0, 6.0, 50, 'first_name 2', 'last_name 2', 'test course 2'), 
                                      (3, 2, 0, 7.0, 70, 'first_name 3', 'last_name 3', 'test course 3'),
                                      (3, 4, 0, 7.0, 100, 'first_name 4', 'last_name 4', 'test course 4')]
        
        result=list(courses_service.get_all_reports(1))
        self.assertIsInstance(result[0], Report)
        self.assertIsInstance(result[1], Report)
        self.assertIsInstance(result[2], Report)
        self.assertIsInstance(result[3], Report)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_reports_by_id(self, mock_read_query):
        mock_read_query.return_value=[(2, 1, 0, 6.0, 25, 'first_name 1', 'last_name 1', 'test course 1')]

        result=list(courses_service.get_reports_by_id(1))
        self.assertIsInstance(result[0], Report)

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_course_by_id_returnCourse_ifExists(self, mock_read_query):
        mock_read_query.side_effect = [
        [
            (1, 'Core Python', 'This is core module', None, 8.0, 1, 'active', 'public'),
        ],
        
        [('python',), ('core',)],
        [('obj 1',), ('obj 2',)],
        ]
        expected_results = Course.from_query_result(
            id=1, title='Core Python', description='This is core module', course_rating=8.0, owner_id = 1, home_page_pic=None, is_active='active', is_premium='public', tags=['python', 'core'], objectives=['obj 1', 'obj 2'])

        result=courses_service.get_course_by_id(1)
        self.assertEqual(result, expected_results)

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
                      is_active='active',
                      is_premium='public',
                      tags=['tag 1', 'tag 2'],
                      objectives=['obj 1', 'obj 2']
                      )
        
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
    def test_get_course_sections_returnlistOfSections_ifCourseExist(self, mock_read_query):
        mock_read_query.return_value=[(1, 'Basics',
                                        'Lorem ipsum dolor',
                                        'Explain the basics',
                                        'ext_link', 1),
                                        (2, 'Basics2',
                                        'Lorem ipsum dolor',
                                        'Explain the basics2',
                                        'ext_link2', 1)]
        result=list(courses_service.get_course_sections(1))
        self.assertIsInstance(result[0], Section)
        self.assertEqual(2, len(result))

    @patch('services.courses_service.read_query', autospec=True)
    def test_get_course_sections_returnEmptylistOfSections_ifNoCourse(self, mock_read_query):
        mock_read_query.return_value=[]
        result=list(courses_service.get_course_sections(100))
        
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

    @patch('services.courses_service.read_query', autospec=True)
    def test_tag_exists_returns_id_if_tag_exists(self, mock_read_query):
        mock_read_query.return_value = [(1,)]  

        tag = 'python'
        result = courses_service.tag_exists(tag)

        self.assertEqual(result, (1,))

    @patch('services.courses_service.read_query', autospec=True)
    def test_tag_exists_returns_none_if_tag_does_not_exist(self, mock_read_query):
        mock_read_query.return_value = [] 

        tag = 'java'
        result = courses_service.tag_exists(tag)

        self.assertIsNone(result)
    
    @patch('services.courses_service.insert_query', autospec=True)
    def test_create_new_tag_inserts_tag_and_returns_tag_id(self, mock_insert_query):
        mock_insert_query.return_value = 1  

        tag = 'python'
        result = courses_service.create_new_tag(tag)

        self.assertEqual(result, 1)
        mock_insert_query.assert_called_once_with("INSERT INTO tags (expertise_area) VALUES (?)", ('python',))

    @patch('services.courses_service.insert_query', autospec=True)
    def test_create_course_tag_inserts_course_and_tag_ids(self, mock_insert_query):
        mock_insert_query.return_value = 1  

        course_id = 1
        tag_id = 2
        result = courses_service.create_course_tag(course_id, tag_id)

        self.assertEqual(result, 1)
        mock_insert_query.assert_called_once_with("INSERT INTO courses_have_tags(courses_id, tags_id) VALUES (?, ?)", (course_id, tag_id))

    @patch('services.courses_service.tag_exists', autospec=True)
    @patch('services.courses_service.create_course_tag', autospec=True)
    @patch('services.courses_service.create_new_tag', autospec=True)
    def test_insert_tags_in_course_calls_tag_exists_and_create_course_tag_for_existing_tags(self, mock_create_new_tag, mock_create_course_tag, mock_tag_exists):
        mock_tag_exists.return_value = [1] 
        course_id = 1
        tags = ['python', 'oop', 'java']

        courses_service.insert_tags_in_course(course_id, tags)

        expected_calls = [
            call('python'),
            call('oop'),
            call('java')
        ]
        mock_tag_exists.assert_has_calls(expected_calls, any_order=True)
        mock_create_course_tag.assert_called_with(course_id, 1)
        mock_create_new_tag.assert_not_called()

    @patch('services.courses_service.tag_exists', autospec=True)
    @patch('services.courses_service.create_course_tag', autospec=True)
    @patch('services.courses_service.create_new_tag', autospec=True)
    def test_insert_tags_in_course_calls_create_new_tag_and_create_course_tag_for_new_tags(
            self, mock_create_new_tag, mock_create_course_tag, mock_tag_exists):
        mock_tag_exists.return_value = None  
        mock_create_new_tag.return_value = 2  
        course_id = 1
        tags = ['python', 'oop', 'java']

        courses_service.insert_tags_in_course(course_id, tags)

        expected_calls = [
            call('python'),
            call('oop'),
            call('java')
        ]
        mock_tag_exists.assert_has_calls(expected_calls, any_order=True)
        mock_create_course_tag.assert_called_with(course_id, 2)
        mock_create_new_tag.assert_called_with('java')

    @patch('services.courses_service.tag_exists', autospec=True)
    @patch('services.courses_service.create_course_tag', autospec=True)
    @patch('services.courses_service.create_new_tag', autospec=True)
    def test_insert_tags_in_course_does_not_call_create_course_tag_when_tags_empty(
            self, mock_create_new_tag, mock_create_course_tag, mock_tag_exists):
        course_id = 1
        tags = []

        courses_service.insert_tags_in_course(course_id, tags)

        mock_tag_exists.assert_not_called()
        mock_create_course_tag.assert_not_called()
        mock_create_new_tag.assert_not_called()

    @patch('services.courses_service.read_query', autospec=True)
    def test_objective_exists_returns_objective_id_if_objective_exists(self, mock_read_query):
        objective = 'Test Objective'
        mock_read_query.return_value = [(1,)]  

        result = courses_service.objective_exists(objective)

        self.assertEqual(result, (1,))  

    @patch('services.courses_service.read_query', autospec=True)
    def test_objective_exists_returns_none_if_objective_does_not_exist(self, mock_read_query):
        objective = 'Non-existent Objective'
        mock_read_query.return_value = []  

        result = courses_service.objective_exists(objective)

        self.assertIsNone(result)  

    @patch('services.courses_service.insert_query', autospec=True)
    def test_create_new_objective_returns_newly_created_objective_id(self, mock_insert_query):
        objective = 'New Objective'
        mock_insert_query.return_value = 1 
    
        result = courses_service.create_new_objective(objective)

        self.assertEqual(result, 1) 
    
    @patch('services.courses_service.objective_exists', autospec=True)
    @patch('services.courses_service.create_course_objective', autospec=True)
    @patch('services.courses_service.create_new_objective', autospec=True)
    def test_insert_objectives_in_course_calls_create_course_objective_for_existing_objectives(
            self, mock_create_new_objective, mock_create_course_objective, mock_objective_exists
    ):
        mock_objective_exists.return_value = [1]
        course_id = 1
        objectives = ['Objective 1', 'Objective 2']

        courses_service.insert_objectives_in_course(course_id, objectives)

        expected_calls = [
            call('Objective 1'),
            call('Objective 2'),
    
        ]
        mock_objective_exists.assert_has_calls(expected_calls, any_order=True)
        mock_create_course_objective.assert_called_with(course_id, 1)
        mock_create_new_objective.assert_not_called()

    @patch('services.courses_service.objective_exists', autospec=True)
    @patch('services.courses_service.create_course_objective', autospec=True)
    @patch('services.courses_service.create_new_objective', autospec=True)
    def test_insert_objectives_in_course_calls_create_new_objective_and_create_course_objective_for_new_objectives(
    
            self, mock_create_new_objective, mock_create_course_objective, mock_objective_exists
    ):
        mock_objective_exists.return_value = None  
        mock_create_new_objective.return_value = 2
        course_id = 1
        objectives = ['Objective 1', 'Objective 2']

        courses_service.insert_objectives_in_course(course_id, objectives)

        expected_calls = [
            call('Objective 1'),
            call('Objective 2'),

        ]
        mock_objective_exists.assert_has_calls(expected_calls, any_order=True)
        mock_create_course_objective.assert_called_with(course_id, 2)
        mock_create_new_objective.assert_called_with('Objective 2')

    @patch('services.courses_service.update_query', autospec=True)
    def test_upload_pic_updates_home_page_pic_for_valid_input(self, mock_update_query):
        course_id = 1
        pic = MagicMock()  

        result = courses_service.upload_pic(course_id, pic)

        mock_update_query.assert_called_once_with("UPDATE courses SET home_page_pic = ? WHERE id = ?", (pic, course_id))
        self.assertEqual(result, mock_update_query.return_value)

    @patch('services.courses_service.update_query', autospec=True)
    def test_upload_pic_returns_none_for_invalid_input(self, mock_update_query):
        course_id = None
        pic = None

        result = courses_service.upload_pic(course_id, pic)

        self.assertIsNone(result)
        self.assertFalse(mock_update_query.called)

    