from feed.tests.abstract_feed_test import AbstractFeedTest


class TestUserUrls(AbstractFeedTest):
    def test_follow_feeds(self):
        self.sample_feed.follow_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.feeds.count(), 1)
        self.assertEqual(self.sample_user2.feeds.count(), 0)

    def test_unfollow_feeds(self):
        self.sample_feed.followers.add(self.sample_user1, self.sample_user2)

        self.sample_feed.remove_follow_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.feeds.count(), 0)
        self.assertEqual(self.sample_user2.feeds.count(), 1)
