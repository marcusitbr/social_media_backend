import os
import requests
import unittest
from config import API_URL
class TestCreateUser(unittest.TestCase):

    API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000/users/')

    def test_create_user(self):
        # Define a sample user payload
        # Define a sample user payload (Modify this data according to your test scenario)

        user_data = {
            "username": "test012",
            "email": "abssasac@example.com",
            "password": "123",
            "is_active": True
        }

        # Send a POST request to create a new user
        response = requests.post(API_URL, json=user_data)

        # Check that the response status code is 201 CREATED
        self.assertEqual(response.status_code, 201, "Failed to create user. Status code: %d" % response.status_code)

        # Check that the response contains the created user data
        self.assertEqual(response.json()["username"], user_data["username"])
        self.assertEqual(response.json()["email"], user_data["email"])
        self.assertEqual(response.json()["is_active"], user_data["is_active"])

    def test_create_user_negative(self):
        # Define invalid user data
        invalid_user_data = {
            "email": "invalid-email",  # Invalid email format
            "password": "123",
            "is_active": True
        }

        # Send a POST request with invalid data
        response = requests.post(API_URL, json=invalid_user_data)

        # Check that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, 422, "Expected status code 400 for invalid user creation")


if __name__ == '__main__':
    unittest.main()

