import json

from django.urls import reverse
from rest_framework import status

from feed.tests.abstract_news_test import AbstractNewsTest


class TestCommentUrls(AbstractNewsTest):
    def test_create_comment(self):
        client = self.api_client

        data = {"text": "working"}
        url = reverse('news-viewset-comments', args=(self.sample_news.id,))
        response = client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.sample_news.comments.count(), 0)

        client, _, _ = self.sign_in_user(client, self.sample_username, self.sample_password)
        response = client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.sample_news.comments.count(), 1)

    def test_list_comments(self):
        client = self.api_client

        url = reverse('news-viewset-detail', args=[self.sample_news.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client, _, _ = self.sign_in_user(client, self.sample_username, self.sample_password)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["comments"]), 0)

        self.sample_news.comments.create(user_id=self.sample_user1.id, text="working")

        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["comments"]), 1)
        self.assertEqual(response.json()["comments"][0]["user"], self.sample_user1.id)
        self.assertEqual(response.json()["comments"][0]["text"], "working")
