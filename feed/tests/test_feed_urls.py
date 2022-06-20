from datetime import datetime

from django.urls import reverse
from rest_framework import status

from feed.models import Feed
from utils.tests import AbstractFeederTest


class TestUserUrls(AbstractFeederTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sample_feed = Feed.objects.create(
            title="Sample Feed - Favorite RSS Related Software & Resources",
            description="Take a look at some of FeedForAll's favorite software and resources for "
                        "learning more about RSS.",
            link="https://www.feedforall.com",
            rss_url="https://www.feedforall.com/sample-feed.xml",
            last_update=datetime(2004, 10, 26, 14, 6, 44)
        )

    def test_list_feeds(self):
        client = self.api_client

        url = reverse('feed-viewset-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client, _, _ = self.sign_in_user(client, self.sample_username, self.sample_password)
        url = reverse('feed-viewset-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_detail_feeds(self):
        client = self.api_client

        url = reverse('feed-viewset-detail', args=[self.sample_feed.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client, _, _ = self.sign_in_user(client, self.sample_username, self.sample_password)
        url = reverse('feed-viewset-detail', args=[self.sample_feed.id])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        feed = response.json()
        self.assertEqual(feed["title"], self.sample_feed.title)
        self.assertEqual(feed["rss_url"], self.sample_feed.rss_url)

    def test_follow_feeds(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(client, self.sample_username, self.sample_password)

        self.assertEqual(user.feeds.count(), 0)
        follow_url = reverse('feed-viewset-follow', args=[self.sample_feed.id])
        response = client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.feeds.count(), 1)

    def test_unfollow_feeds(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(client, self.sample_username, self.sample_password)

        user.feeds.add(self.sample_feed)
        self.assertEqual(user.feeds.count(), 1)
        follow_url = reverse('feed-viewset-follow', args=[self.sample_feed.id])
        response = client.delete(follow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(user.feeds.count(), 0)

    def test_user_followed_feeds(self):
        client = self.api_client
        client, user, _ = self.sign_in_user(client, self.sample_username, self.sample_password)

        followed_by_user_url = reverse('feed-viewset-followed')
        response = client.get(followed_by_user_url)
        self.assertEqual(len(response.json()), 0)

        follow_url = reverse('feed-viewset-follow', args=[self.sample_feed.id])
        response = client.post(follow_url)

        followed_by_user_url = reverse('feed-viewset-followed')
        response = client.get(followed_by_user_url)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], self.sample_feed.id)
