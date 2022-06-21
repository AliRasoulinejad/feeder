import json

from django.urls import reverse
from rest_framework import status

from utils.tests import AbstractFeederTest


class TestUserUrls(AbstractFeederTest):
    def test_signup_user(self):
        data = {
            "first_name": "ali",
            "last_name": "rasouli",
            "email": "a@a.com",
            "username": "test1",
            "password": "@Aaalkuvj",
            "password2": "@Aaalkuvj",
        }
        response = self.api_client.post(
            reverse("user-signup"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        data = {
            "username": self.sample_username,
            "password": self.sample_password,
        }
        response = self.api_client.post(
            reverse("signin-token"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        client, _, refresh = self.sign_in_user(
            self.api_client, self.sample_username, self.sample_password
        )
        data = {"refresh": refresh}
        response = self.api_client.post(
            reverse("refresh-token"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
