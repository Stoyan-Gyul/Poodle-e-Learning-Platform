from unittest import TestCase
from unittest.mock import patch

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