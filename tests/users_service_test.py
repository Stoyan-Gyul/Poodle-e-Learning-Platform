from unittest import TestCase
from unittest import mock
from unittest.mock import patch, ANY

from data.models import User
from services import users_service

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
        
        user = User(
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
            verification_token='token',
            phone='1234567890',
            linked_in_account='linkedin'
        )
        
        actual_id  = users_service.create_new_user(user)
    
        
        self.assertEqual(actual_id, expected_id)
        
        mock_insert_query.assert_any_call(
            "INSERT INTO users (email, password, role, first_name, last_name, verification_token, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?);",
            ('test@example.com', mock.ANY, 'user', 'John', 'Doe', 'token', 0)
        )
        
        mock_insert_query.assert_any_call(
            "INSERT INTO teachers (users_id, phone, linked_in_account) VALUES (?, ?, ?)",
            (1, '1234567890', 'linkedin')
        )

        self.assertEqual(mock_insert_query.call_count, 2)

        mock_insert_query.assert_called_with(
            "INSERT INTO teachers (users_id, phone, linked_in_account) VALUES (?, ?, ?)",
            (1, '1234567890', 'linkedin')
        )
    
    def test_createNewUser_with_noneUser_returns_None(self):

        result = users_service.create_new_user(None)
        
        self.assertIsNone(result)  


    @patch('services.users_service.bcrypt.checkpw', autospec=True)
    def test_try_login_with_valid_credentials_returns_user(self, mock_checkpw):
    
        user = User(
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
            verification_token='token',
        )
        
        mock_checkpw.return_value = True
        
        actual_user = users_service.try_login(user, 'password')
        
        self.assertEqual(actual_user, user)
        
        mock_checkpw.assert_called_once_with(
            'password'.encode('utf-8'),
            user.password.encode('utf-8')
        )

    @patch('services.users_service.bcrypt.checkpw', autospec=True)
    def test_tryLogin_with_invalid_credentials_returns_none(self, mock_checkpw):
        user = User(
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
            verification_token='token',
        )
        
        mock_checkpw.return_value = False
        
        result = users_service.try_login(user, 'wrong_password')
        
        self.assertIsNone(result)
        
        mock_checkpw.assert_called_once_with(
            'wrong_password'.encode('utf-8'),
            user.password.encode('utf-8')
        )

    def test_try_login_with_none_user_returns_none(self):
        
        result = users_service.try_login(None, 'password')
        
        self.assertIsNone(result) 

    def test_try_login_with_none_password_returns_none(self):

        user = User(
            email='test@example.com',
            password='password',
            role='user',
            first_name='John',
            last_name='Doe',
            verification_token='token',
        )
        
        result = users_service.try_login(user, None)
        
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
