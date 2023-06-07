import time
from unittest import TestCase
from unittest import mock
from unittest.mock import MagicMock, patch, ANY

import jwt

from data.common.models.user import User
from data.common.models.view_courses import ViewUserCourse
from data.common.models.update_data import UpdateData
# from services.users_service import Teacher
from services import users_service


USER = User(
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
            verification_token='token',
            phone='1234567890',
            linked_in_account='linkedin'
        )

NEW_DATA=UpdateData(
                    password='pass',
                    first_name='fname',
                    last_name='lname',
                    role='teacher',
                    phone='0098',
                    linked_in_account='www.sdfsd.sdf')

class UserService_Should(TestCase):
    
    @patch('services.users_service.read_query', autospec=True)
    def test_findById_returnsUser_when_userExists(self, mock_read_query):
        expected_data = [(1, 'ani@abv.bg', '$2b$12$Eb0aKvsM/YGeLbsbGEXvU.ztXQ8uNIygejK213iYLVJT1PwuPFIt6', 'ani', 'ivanova', 'user')]
        
        mock_read_query.return_value = expected_data
        actual_data = users_service.find_by_id(1)

        self.assertIsInstance(actual_data, User)
        self.assertEqual(expected_data[0][0], actual_data.id)
        self.assertEqual(expected_data[0][1], actual_data.email)
        self.assertEqual(expected_data[0][2], actual_data.password)
        self.assertEqual(expected_data[0][3], actual_data.first_name)
        self.assertEqual(expected_data[0][4], actual_data.last_name)
        self.assertEqual(expected_data[0][5], actual_data.role)

    
    @patch('services.users_service.read_query', autospec=True)
    def test_findById_returnsNone_when_userDoesNotExist(self, mock_read_query):
        mock_read_query.return_value = []
        actual_data = users_service.find_by_id(1)

        self.assertIsNone(actual_data)
    
    def test_findById_returnsNone_when_idIsNone(self):
        actual_data = users_service.find_by_id(None)

        self.assertIsNone(actual_data)
    

    @patch('services.users_service.read_query', autospec=True)
    def test_findByEmail_returnsUser_when_userExists(self, mock_read_query):
        expected_data = [(1, 'ani@abv.bg', '$2b$12$Eb0aKvsM/YGeLbsbGEXvU.ztXQ8uNIygejK213iYLVJT1PwuPFIt6', 'ani', 'ivanova', 'user')]
        
        mock_read_query.return_value = expected_data
        actual_data = users_service.find_by_id(1)

        self.assertIsInstance(actual_data, User)
        self.assertEqual(expected_data[0][0], actual_data.id)
        self.assertEqual(expected_data[0][1], actual_data.email)
        self.assertEqual(expected_data[0][2], actual_data.password)
        self.assertEqual(expected_data[0][3], actual_data.first_name)
        self.assertEqual(expected_data[0][4], actual_data.last_name)
        self.assertEqual(expected_data[0][5], actual_data.role)

    
    @patch('services.users_service.read_query', autospec=True)
    def test_findByEmail_returnsNone_when_userDoesNotExist(self, mock_read_query):
        mock_read_query.return_value = []
        actual_data = users_service.find_by_id(1)

        self.assertIsNone(actual_data)
    
    def test_findByEmail_returnsNone_when_idIsNone(self):
        actual_data = users_service.find_by_id(None)

        self.assertIsNone(actual_data)
    
    
    @patch('services.users_service.insert_query', autospec=True)
    def test_createNewUser_returnsUserID_create_student(self, mock_insert_query):
        expected_id = 1
        mock_insert_query.return_value = 1  
        
        user = User(
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
            verification_token='token',
        )
        
        actual_id  = users_service.create_new_user(user)
    
        
        self.assertEqual(actual_id, expected_id)
        
        mock_insert_query.assert_any_call(
            "INSERT INTO users (email, password, role, first_name, last_name, verification_token, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?);",
            ('test@example.com', mock.ANY, 'user', 'John', 'Doe', 'token', 0)
        )
        
        self.assertEqual(mock_insert_query.call_count, 1)

        mock_insert_query.assert_called_once_with(
            "INSERT INTO users (email, password, role, first_name, last_name, verification_token, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?);",
            ('test@example.com', mock.ANY, 'user', 'John', 'Doe', 'token', 0)
        )
    
    @patch('services.users_service.insert_query', autospec=True)
    def test_createNewUser_returnsUserID_create_teacher(self, mock_insert_query):
        expected_id = 1
        mock_insert_query.return_value = 1  
        
        actual_id  = users_service.create_new_user(USER)
    
        
        self.assertEqual(actual_id, expected_id)
        
        mock_insert_query.assert_any_call(
            "INSERT INTO users (email, password, role, first_name, last_name, verification_token, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?);",
            ('test@example.com', mock.ANY, 'user', 'John', 'Doe', 'token', 0)
        )
        
        mock_insert_query.assert_any_call(
            "INSERT INTO teachers (users_id, phone_number, linked_in_account) VALUES (?, ?, ?)",
            (1, 1234567890, 'linkedin')
        )

        self.assertEqual(mock_insert_query.call_count, 2)

        mock_insert_query.assert_called_with(
            "INSERT INTO teachers (users_id, phone_number, linked_in_account) VALUES (?, ?, ?)",
            (1, 1234567890, 'linkedin')
        )
    
    def test_createNewUser_with_noneUser_returns_None(self):

        result = users_service.create_new_user(None)
        
        self.assertIsNone(result)  


    @patch('services.users_service.bcrypt.checkpw', autospec=True)
    def test_try_login_with_valid_credentials_returns_user(self, mock_checkpw):
    
        # user = User(
        #     email='test@example.com',
        #     password='password',
        #     role='user',
        #     first_name='John',
        #     last_name='Doe',
        #     verification_token='token',
        # )
        
        mock_checkpw.return_value = True
        
        actual_user = users_service.try_login(USER, 'password')
        
        self.assertEqual(actual_user, USER)
        
        mock_checkpw.assert_called_once_with(
            'password'.encode('utf-8'),
            USER.password.encode('utf-8')
        )

    @patch('services.users_service.bcrypt.checkpw', autospec=True)
    def test_tryLogin_with_invalid_credentials_returns_none(self, mock_checkpw):
        # user = User(
        #     email='test@example.com',
        #     password='password',
        #     role='user',
        #     first_name='John',
        #     last_name='Doe',
        #     verification_token='token',
        # )
        
        mock_checkpw.return_value = False
        
        result = users_service.try_login(USER, 'wrong_password')
        
        self.assertIsNone(result)
        
        mock_checkpw.assert_called_once_with(
            'wrong_password'.encode('utf-8'),
            USER.password.encode('utf-8')
        )

    def test_try_login_with_none_user_returns_none(self):
        
        result = users_service.try_login(None, 'password')
        
        self.assertIsNone(result) 

    def test_try_login_with_none_password_returns_none(self):

        # user = User(
        #     email='test@example.com',
        #     password='password',
        #     role='user',
        #     first_name='John',
        #     last_name='Doe',
        #     verification_token='token',
        # )
        
        result = users_service.try_login(USER, None)
        
        self.assertIsNone(result)
    
    @patch('services.users_service.jwt.encode', autospec=True)
    def test_generate_token_with_valid_user(self, mock_encode):

        user = User(
            id=123,
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
        )
        
        mock_encode.return_value = 'mocked_token'
        
        actual_token = users_service.generate_token(user)
        
        self.assertEqual(actual_token, 'mocked_token')
        
        mock_encode.assert_called_once_with(
            {
                'user_id': 123,
                'email': 'test@example.com',
                'role': 'user',
                'exp': mock.ANY
            },
            mock.ANY,
            algorithm='HS256'
        )

    def test_generate_token_with_none_user(self):
    
        result = users_service.generate_token(None)

        self.assertIsNone(result)


    @patch('services.users_service.jwt.decode', autospec=True)
    def test_validate_token_with_valid_token(self, mock_decode):
        current_time = int(time.time()) 
        expiration_time = current_time + 30 * 60
        
        mock_decode.return_value = {
            'user_id': 123,
            'email': 'test@example.com',
            'role': 'user',
            'exp': expiration_time
        }
        
        actual_user_info = users_service.validate_token('valid_token')
        
        self.assertEqual(actual_user_info, [123, 'test@example.com', 'user'])  

        mock_decode.assert_called_once_with(
            'valid_token',
            mock.ANY,
            algorithms=['HS256']
        )

    def test_validate_token_with_none_token(self):

        result = users_service.validate_token(None)
        
        self.assertIsNone(result)

    @patch('services.users_service.jwt.decode', autospec=True)
    def test_validate_token_with_expired_token(self, mock_decode):
    
        mock_decode.side_effect = jwt.ExpiredSignatureError('Expired token')
        
        result = users_service.validate_token('expired_token')
        
        self.assertIsNone(result)
        
        mock_decode.assert_called_once_with(
            'expired_token',
            mock.ANY,
            algorithms=['HS256']
        )

    @patch('services.users_service.jwt.decode', autospec=True)
    def test_validate_token_with_invalid_token(self, mock_decode):

        mock_decode.side_effect = jwt.InvalidTokenError('Invalid token')
        
        result = users_service.validate_token('invalid_token')
        
        self.assertIsNone(result)
        
        mock_decode.assert_called_once_with(
            'invalid_token',
            mock.ANY,
            algorithms=['HS256']
        )
    
    @patch('services.users_service.update_query', autospec=True)
    def test_subscribe_to_course_with_valid_parameters(self, mock_update_query):
        expected = 1
        mock_update_query.return_value = 1

        result = users_service.subscribe_to_course(123, 456)

        self.assertEqual(expected, result)

        mock_update_query.assert_called_once_with(
            "INSERT INTO users_have_courses (users_id, courses_id, status) VALUES (?, ?, ?)",
            (123, 456, 0)
        )

    @patch('services.users_service.update_query', autospec=True)
    def test_subscribe_to_course_with_none_parameters(self, mock_update_query):
        
        result = users_service.subscribe_to_course(None, None)

        self.assertIsNone(result)

        mock_update_query.assert_not_called()
    
    @patch('services.users_service.update_query', autospec=True)
    def test_unsubscribe_to_course_with_valid_parameters(self, mock_update_query):
        expected = 1
        mock_update_query.return_value = 1

        result = users_service.unsubscribe_from_course(123, 456)

        self.assertEqual(expected, result)

        mock_update_query.assert_called_once_with(
            "UPDATE users_have_courses SET status = ? WHERE users_id = ? AND courses_id = ?",
            (2, 123, 456)
        )

    @patch('services.users_service.update_query', autospec=True)
    def test_unsubscribe_to_course_with_none_parameters(self, mock_update_query):
        
        result = users_service.unsubscribe_from_course(None, None)

        self.assertIsNone(result)

        mock_update_query.assert_not_called()
    
    @patch('services.users_service.smtplib.SMTP', autospec=True)
    def test_send_verification_email(self, mock_smtp):
        
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        mock_server.starttls = MagicMock()

        result = users_service.send_verification_email("test@example.com", "http://example.com/verification")

        self.assertEqual(result, "Verification email sent successfully.")

    @patch('services.users_service.read_query')
    @patch('services.users_service.update_query')
    def test_verify_email_with_valid_token_returns_True(self, mock_update_query, mock_read_query):
        
        mock_read_query.return_value = [('token',)]

        result = users_service.verify_email("test@example.com", "token")

        self.assertTrue(result)
    
        mock_read_query.assert_called_once_with("SELECT verification_token FROM users WHERE email = ?", ("test@example.com",))
        mock_update_query.assert_called_once_with("UPDATE users SET is_verified = ? WHERE email = ?", (1, "test@example.com"))

    @patch('services.users_service.read_query')
    @patch('services.users_service.update_query')
    def test_verify_email_with_invalid_token_returns_False(self, mock_update_query, mock_read_query):

        mock_read_query.return_value = [('invalid_token',)]

        result = users_service.verify_email("test@example.com", "token")

        self.assertFalse(result) 

        mock_read_query.assert_called_once_with("SELECT verification_token FROM users WHERE email = ?", ("test@example.com",))
        mock_update_query.assert_not_called()

    @patch('services.users_service.read_query')
    @patch('services.users_service.update_query')
    def test_verify_email_with_none_parameters_returns_None(self, mock_update_query, mock_read_query):
        
        result = users_service.verify_email(None, None)

        self.assertIsNone(result)

        mock_read_query.assert_not_called()
        mock_update_query.assert_not_called()


    @patch('services.users_service.read_query')
    def test_view_teacher_returnTeacher_when_teacher_addsExists(self, mock_read_query):
        mock_read_query.return_value=[('08882412', 'https://www.linkedin.com/aliceparker/')]
        
        result=users_service.view_teacher(USER)
        self.assertIsInstance(result,User)

    @patch('services.users_service.read_query')
    def test_view_teacher_returnUser_if_No_teacher_adds(self, mock_read_query):
        mock_read_query.return_value=[]
        
        result=users_service.view_teacher(USER)
        self.assertIsInstance(result,User)

    def test_update_user_returnNone_ifNo_user(self):
        user=None
        
        result=users_service.update_user(user,NEW_DATA)
        self.assertIsNone(result)

    def test_update_user_returnNone_ifNo_updateData(self):
        new_data=None
        
        result=users_service.update_user(USER,new_data)
        self.assertIsNone(result)

    @patch('services.users_service.update_query')
    def test_update_user_returnFalse_if_data_not_updated(self, mock_update_query):
        mock_update_query.return_value=False
        
        result=users_service.update_user(USER,NEW_DATA)
        self.assertEqual(False, result)

    @patch('services.users_service.update_query')
    def test_update_user_returnTrue_if_data_updated(self, mock_update_query):
        mock_update_query.return_value=True
        
        result=users_service.update_user(USER,NEW_DATA)
        self.assertEqual(True, result)
    
    @patch('services.users_service.update_query')
    def test_admin_approves_user_returnTrue_iftransactionOK(self, mock_update_query):
        mock_update_query.return_value=True
        result=users_service.admin_approves_user(2)
        self.assertEqual(True, result)

    @patch('services.users_service.update_query')
    def test_admin_approves_user_returnFalse_iftransaction_notOK(self, mock_update_query):
        mock_update_query.return_value=False
        result=users_service.admin_approves_user(2)
        self.assertEqual(False, result)

    @patch('services.users_service.update_query')
    def test_admin_disapproves_user_returnTrue_iftransactionOK(self, mock_update_query):
        mock_update_query.return_value=True
        result=users_service.admin_approves_user(2)
        self.assertEqual(True, result)

    @patch('services.users_service.update_query')
    def test_admin_disapproves_user_returnFalse_iftransaction_notOK(self, mock_update_query):
        mock_update_query.return_value=False
        result=users_service.admin_approves_user(2)
        self.assertEqual(False, result)

    @patch('services.users_service.update_query')
    def test_approve_enrollment_returnTrue_iftransactionOK(self, mock_update_query):
        mock_update_query.return_value=True
        result=users_service.approve_enrollment(2,1)
        self.assertEqual(True, result)

    @patch('services.users_service.update_query')
    def test_approve_enrollment_returnFalse_iftransaction_notOK(self, mock_update_query):
        mock_update_query.return_value=False
        result=users_service.approve_enrollment(2,1)
        self.assertEqual(False, result)

    @patch('services.users_service.update_query')
    def test_approve_enrollment_returnNone_ifstudentidNone(self, mock_update_query):
        mock_update_query.return_value=False
        result=users_service.approve_enrollment(None,1)
        self.assertIsNone(result)

    @patch('services.users_service.update_query')
    def test_approve_enrollment_returnNone_ifcourseidNone(self, mock_update_query):
        mock_update_query.return_value=False
        result=users_service.approve_enrollment(2,None)
        self.assertIsNone(result)

    @patch('services.users_service.read_query')
    def test_view_admin_return_listOfUsers(self, mock_read_query):
        mock_read_query.return_value=[(1, 'alice@abv.bg', '$2b$12$Xag4rXZGOJrNkwRb32N6s.nscNQFlIfJSYhJXgHrFebVGgjj8Ve9K', 'alice', 'Parker100', 'teacher', '0888345600', 'www.linkedin.com/aliceparker100', None, 0, 1),
                                      (2, 'steven@abv.bg', '$2b$12$ooercgclJ9NziweYJC8nSunM8LJ43PE0EvxTv8cul/7kdNTolGqMm', 'Steven', 'Parker100', 'student', None, None, None, 0, 1),
                                      (3, 'steven1@abv.bg', '$2b$12$yUT0WH0qklpI15Y7jXqyVe3.j6DCJVo4HsjrYBdIoLTB684/YLBTu', 'Steven1', 'Parker1', 'student', None, None, None, 1, 1),
                                      (4, 'steven2@abv.bg', '$2b$12$3cUVOilSyrfMNZ5LjPUKT.68P/OY7qVYL/VrVM6mpWUTx192xza8K', 'steven2', 'parker2', 'student', None, None, 'e399f595-5312-4ba1-bb74-64c46dc5bcd2', 1, 0),
                                      (5, 'admin@abv.bg', '$2b$12$at3uULHSgb2zV6nrIJLP7uuSITMvZbMw68gA54Lfpy9OvV7saevaO', 'admin', 'adminov', 'admin', None, None, '77dc7699-4e3f-448a-9133-fb676d8b373b', 0, 1)]
        
        result=list(users_service.view_admin())
        self.assertEqual(5,len(result))
        self.assertIsInstance(result[0], User)

    @patch('services.users_service.read_query')
    def test_view_admin_return_EmptyListOfNoUsers(self, mock_read_query):
        mock_read_query.return_value=[]
        
        result=list(users_service.view_admin())
        self.assertEqual(0,len(result))

    @patch('services.users_service.read_query')
    def test_view_all_pending_approval_student_return_listOfViewUserCourse(self, mock_read_query):
        mock_read_query.return_value=[(2, 'Steven', 'Parker100', 2, 'OOP'),
                                      (3, 'Steven1', 'Parker1', 2, 'OOP'),
                                      (2, 'Steven', 'Parker100', 4, 'General Python'),
                                      (3, 'Steven1', 'Parker1', 4, 'General Python')]
        result=list(users_service.view_all_pending_approval_students(1))
        self.assertEqual(4,len(result))
        self.assertIsInstance(result[0], ViewUserCourse)

    @patch('services.users_service.read_query')
    def test_view_all_pending_approval_student_return_EmptyListifNoUsersInCourses(self, mock_read_query):
        mock_read_query.return_value=[]
        result=list(users_service.view_all_pending_approval_students(1))
        self.assertEqual(0,len(result))

    @patch('services.users_service.read_query')
    def test_get_teacher_info_with_course_id_return_list(self, mock_read_query):
        mock_read_query.return_value=[('alice@abv.bg', 'alice', 'Parker100', 'Core Python')]
        result=list(users_service.get_teacher_info_with_course_id(1))
        self.assertEqual(1,len(result))
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)

    @patch('services.users_service.read_query')
    def test_get_teacher_info_with_course_id_return_None_ifcourseidNone(self, mock_read_query):
        mock_read_query.return_value=[('alice@abv.bg', 'alice', 'Parker100', 'Core Python')]
        result=users_service.get_teacher_info_with_course_id(None)
        self.assertIsNone(result)

    @patch('services.users_service.smtplib.SMTP', autospec=True)
    def test_send_student_enrolled_in_course_email_to_teacher_return_string(self, mock_smtp):
        mock_server=MagicMock()
        mock_smtp.return_value= mock_server
        mock_server.starttls = MagicMock()

        result=users_service.send_student_enrolled_in_course_email_to_teacher("test@example.com",
                                                                              "http://example.com/verification",
                                                                              'alice',
                                                                              'parker',
                                                                              'python')
        self.assertEqual(result, "Verification email sent successfully.")
        
    
    
    
    

      
        


