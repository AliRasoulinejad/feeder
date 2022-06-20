from datetime import datetime
from unittest import mock

import feedparser

from feed.models import Feed, News
from feed.scraper import Scraper, FeedUpdater, RSSJsonFeedParser, RSSJsonItemParser
from feed.tests.abstract_feed_test import AbstractFeedTest


class TestScraper(AbstractFeedTest):
    def test_scraper(self):
        url = "https://www.feedforall.com/sample-feed.xml"
        scraper = Scraper.parse(url)
        fp = feedparser.parse(url)

        self.assertEqual(scraper.feed, fp.feed)
        self.assertEqual(scraper.items, fp.entries)

    def test_updater_check_for_update(self):
        updater = FeedUpdater(self.sample_feed).update()
        self.assertFalse(updater)

    @mock.patch("feed.scraper.FeedUpdater._check_for_update", side_effect=lambda: True)
    def test_updater(self, *args, **kwargs):
        updater = FeedUpdater(self.sample_feed).update()
        self.assertTrue(updater)

    def test_rss_json_feed_parser(self, *args, **kwargs):
        rss_url = "https://www.feedforall.com/sample.xml"
        fake_feed = Feed.objects.create(
            title="fake title",
            description="fake description",
            link="https://www.feedforall.com/fake",
            rss_url=rss_url,
            last_update=datetime(2004, 10, 20, 11, 56, 48)
        )

        scraper = Scraper.parse(rss_url)
        RSSJsonFeedParser(fake_feed).update_feed(scraper.feed)

        fake_feed.refresh_from_db()
        self.assertEqual(fake_feed.title, "FeedForAll Sample Feed")
        self.assertEqual(fake_feed.link, "http://www.feedforall.com/industry-solutions.htm")

    def test_rss_json_items_parser(self, *args, **kwargs):
        self.assertEqual(News.objects.count(), 0)
        scraper = Scraper.parse(self.sample_feed.rss_url)
        RSSJsonItemParser(self.sample_feed).insert_news(scraper.items)

        self.assertEqual(News.objects.count(), len(scraper.items))
        self.assertEqual(News.objects.first().title, "RSS Resources")
        self.assertEqual(News.objects.first().link, "http://www.feedforall.com")
