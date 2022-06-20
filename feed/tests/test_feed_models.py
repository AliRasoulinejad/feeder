from datetime import datetime

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

    def test_follow_feeds(self):
        self.sample_feed.follow_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.feeds.count(), 1)
        self.assertEqual(self.sample_user2.feeds.count(), 0)

    def test_unfollow_feeds(self):
        self.sample_feed.followers.add(self.sample_user1, self.sample_user2)

        self.sample_feed.remove_follow_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.feeds.count(), 0)
        self.assertEqual(self.sample_user2.feeds.count(), 1)
