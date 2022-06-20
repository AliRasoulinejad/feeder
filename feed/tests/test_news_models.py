from feed.tests.abstract_news_test import AbstractNewsTest


class TestUserUrls(AbstractNewsTest):
    def test_read_news(self):
        self.sample_news.read_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.read_news.filter(news_id=self.sample_news.id).count(), 1)
        self.assertEqual(self.sample_user2.read_news.filter(news_id=self.sample_news.id).count(), 0)

    def test_bookmark_news(self):
        self.sample_news.bookmark_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.bookmarked_news.filter(news_id=self.sample_news.id).count(), 1)
        self.assertEqual(self.sample_user2.bookmarked_news.filter(news_id=self.sample_news.id).count(), 0)

    def test_remove_bookmark_news(self):
        self.sample_news.bookmarked_by.add(self.sample_user1, self.sample_user2)

        self.sample_news.remove_bookmark_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.bookmarked_news.filter(
            news_id=self.sample_news.id).count(), 0)
        self.assertEqual(self.sample_user2.bookmarked_news.filter(
            news_id=self.sample_news.id).count(), 1)

    def test_favorite_news(self):
        self.sample_news.favorite_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.favorites_news.filter(
            news_id=self.sample_news.id).count(), 1)
        self.assertEqual(self.sample_user2.favorites_news.filter(
            news_id=self.sample_news.id).count(), 0)

    def test_remove_favorite_news(self):
        self.sample_news.favorite_by.add(self.sample_user1, self.sample_user2)

        self.sample_news.remove_favorite_by_user_id(self.sample_user1.id)
        self.assertEqual(self.sample_user1.favorites_news.filter(
            news_id=self.sample_news.id).count(), 0)
        self.assertEqual(self.sample_user2.favorites_news.filter(
            news_id=self.sample_news.id).count(), 1)
