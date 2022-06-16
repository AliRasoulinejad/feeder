import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class AbstractFeederTest(TestCase):
    def setUp(self) -> None:
        self.populate_db()

    def populate_db(self):
        self.api_client = APIClient()

    def sign_in_user(self, client, username, password):
        data = {"username": username, "password": password}
        response = client.post(
            reverse("signin-token"), json.dumps(data), content_type="application/json"
        )
        token = response.json()["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client
