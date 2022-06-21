from datetime import datetime

from django.urls import reverse
from rest_framework import status

from feed.models import News
from feed.tests.abstract_news_test import AbstractNewsTest


class TestNewsUrls(AbstractNewsTest):
    def test_list_news(self):
        client = self.api_client

        url = reverse("news-viewset-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )
        url = reverse("news-viewset-list")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(News.objects.count(), 1)

        self.sample_feed.follow_by_user_id(user_id=user.id)
        News.objects.create(
            feed_id=self.sample_feed.id,
            title="Recommended Desktop Feed Reader Software",
            description="""<b>FeedDemon</b> enables you to be quick""",
            link="https://www.feedforall.com/feedforall-partners.htm",
            author="",
            published_at=datetime(2004, 10, 26, 14, 3, 25),
        )
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(News.objects.count(), 2)

    def test_detail_news(self):
        client = self.api_client

        url = reverse("news-viewset-detail", args=[self.sample_news.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client, _, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )
        url = reverse("news-viewset-detail", args=[self.sample_news.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        news = response.json()
        self.assertEqual(news["title"], self.sample_news.title)
        self.assertEqual(news["feed"], self.sample_news.feed_id)

    def test_read_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        self.assertEqual(user.read_news.count(), 0)
        follow_url = reverse("news-viewset-read", args=[self.sample_news.id])
        response = client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.read_news.count(), 1)

    def test_bookmark_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        self.assertEqual(user.bookmarks.count(), 0)
        follow_url = reverse("news-viewset-bookmark", args=[self.sample_news.id])
        response = client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.bookmarks.count(), 1)

    def test_remove_bookmarked_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        user.bookmarks.add(self.sample_news)
        self.assertEqual(user.bookmarks.count(), 1)
        follow_url = reverse("news-viewset-bookmark", args=[self.sample_news.id])
        response = client.delete(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.bookmarks.count(), 0)

    def test_favorite_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        self.assertEqual(user.favorites.count(), 0)
        follow_url = reverse("news-viewset-favorite", args=[self.sample_news.id])
        response = client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.favorites.count(), 1)

    def test_remove_favorites_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        user.favorites.add(self.sample_news)
        self.assertEqual(user.favorites.count(), 1)
        follow_url = reverse("news-viewset-favorite", args=[self.sample_news.id])
        response = client.delete(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.favorites.count(), 0)

    def test_user_bookmarked_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        followed_by_user_url = reverse("news-viewset-bookmarks")
        response = client.get(followed_by_user_url)
        self.assertEqual(len(response.json()), 0)

        follow_url = reverse("news-viewset-bookmark", args=[self.sample_news.id])
        response = client.post(follow_url)

        followed_by_user_url = reverse("news-viewset-bookmarks")
        response = client.get(followed_by_user_url)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.sample_news.id)

    def test_user_favorite_news(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(
            client, self.sample_username, self.sample_password
        )

        followed_by_user_url = reverse("news-viewset-favorites")
        response = client.get(followed_by_user_url)
        self.assertEqual(len(response.json()), 0)

        follow_url = reverse("news-viewset-favorite", args=[self.sample_news.id])
        response = client.post(follow_url)

        followed_by_user_url = reverse("news-viewset-favorites")
        response = client.get(followed_by_user_url)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.sample_news.id)
