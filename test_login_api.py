import requests
import unittest
from unittest.mock import patch

class TestLoginAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://mockapi.test"
        self.login_endpoint = f"{self.base_url}/login"

    @patch('requests.post')
    def test_successful_login(self, mock_post):
        # Mock successful response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }

        response = requests.post(
            self.login_endpoint,
            json={
                "username": "testuser",
                "password": "Pass123!"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertTrue(len(response.json()['token']) > 0)

    @patch('requests.post')
    def test_invalid_credentials(self, mock_post):
        # Mock unauthorized response
        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = {
            "error": "Invalid credentials"
        }

        response = requests.post(
            self.login_endpoint,
            json={
                "username": "testuser",
                "password": "wrongpass"
            }
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid credentials')

    @patch('requests.post')
    def test_invalid_request_format(self, mock_post):
        # Mock bad request response
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            "error": "Missing required fields"
        }

        response = requests.post(
            self.login_endpoint,
            json={"username": "testuser"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

if __name__ == '__main__':
    unittest.main()