from unittest import mock

from feed.tests.abstract_feed_test import AbstractFeedTest


def make_exception():
    """A function that use for testing backoff mechanism"""
    raise Exception('An exception for testing')


class TestTasks(AbstractFeedTest):

    @mock.patch("feed.scraper.FeedUpdater.update", side_effect=make_exception)
    def test_update_feed_failure(self, *args, **kwargs):
        from feed.tasks import update_feed

        task = update_feed.delay(feed_id=self.sample_feed.id)
        self.assertEqual(task.status, 'FAILURE')

    def test_update_feed_success(self, *args, **kwargs):
        from feed.tasks import update_feed

        task = update_feed.delay(feed_id=self.sample_feed.id)
        self.assertEqual(task.status, 'SUCCESS')
