
import os
import requests
import unittest
import pytest

class LoginScenario(unittest.TestCase):
    LOGIN_URL = os.getenv('LOGIN_URL', 'http://127.0.0.1:8000/login')

    def login_scenario(self, user_credentials):
        # Send a POST request to the login endpoint with the user credentials
        response = requests.post(self.LOGIN_URL, json=user_credentials)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the access token from the response
            access_token = response.json()["access_token"]
            token_type = response.json()["token_type"]
            return {"access_token": access_token, "token_type": token_type}
        else:
            # Return the error details if login failed
            return {"status_code": response.status_code, "detail": response.json().get("detail", "No detail provided")}

    def test_login_success(self):
        # Define the correct user credentials
        user_credentials = {
            "username": "petya",
            "email": "petya@example.com",
            "password": "petya",
            "is_active": True
        }
        
        login_data = self.login_scenario(user_credentials)
        assert "access_token" in login_data, "Login failed"
        print("Login successful!")
        print("Access Token:", login_data["access_token"])
        print("Token Type:", login_data["token_type"])

    def test_login_failure(self):
        # Define the incorrect user credentials
        user_credentials = {
            "username": "wrong_username",
            "email": "wrong_email@example.com",
            "password": "wrong_password",
            "is_active": False
        }

        login_data = self.login_scenario(user_credentials)
        assert "access_token" not in login_data, "Login unexpectedly succeeded"
        assert login_data["status_code"] == 401, "Expected status code 401, got {}".format(login_data["status_code"])
        print("Login failed as expected.")
        print("Error Detail:", login_data["detail"])

if __name__ == '__main__':
    unittest.main()
