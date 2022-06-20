import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from user.models import User


class AbstractFeederTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()

        cls.sample_username = "user"
        cls.sample_password = "@#TeSt"
        cls.sample_user1 = User.objects.create_user(
            username=cls.sample_username,
            email="test@test.com",
            password=cls.sample_password
        )
        cls.sample_user2 = User.objects.create_user(
            username="user2",
            email="test2@test2.com",
            password="B$TeSt2"
        )

    @staticmethod
    def sign_in_user(client, username, password):
        data = {"username": username, "password": password}
        response = client.post(
            reverse("signin-token"), json.dumps(data), content_type="application/json"
        )
        access_token = response.json()["access"]
        refresh_token = response.json()["refresh"]
        user = User.objects.get(username=username)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return client, user, refresh_token
