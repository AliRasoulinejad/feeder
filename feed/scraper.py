import feedparser
import pytz
from dateutil.parser import parse

from feed.models import News, Feed


class Scraper:
    def __init__(self, feed, items):
        self.feed = feed
        self.items = items

    @classmethod
    def parse(cls, url):
        parsed_url = feedparser.parse(url)
        return cls(feed=parsed_url.feed, items=parsed_url.entries)


class FeedUpdater:
    def __init__(self, feed: Feed):
        self.feed = feed
        self.scraper = Scraper.parse(feed.rss_url)

    def update(self):
        if not self._check_for_update():
            return False

        RSSJsonFeedParser(self.feed).update_feed(self.scraper.feed)
        RSSJsonItemParser(self.feed).insert_news(self.scraper.items)
        return True

    def _check_for_update(self):
        last_update_str = self.scraper.feed.get("updated")
        last_update = parse(last_update_str)
        utc = pytz.UTC
        return (
                self.feed.last_update is not None
                and last_update is not None
                and self.feed.last_update.replace(tzinfo=utc) >= last_update
        )


# TODO: rename
class RSSJsonFeedParser:
    def __init__(self, feed: Feed):
        self.feed = feed

    def update_feed(self, json_feed):
        self.feed.title = json_feed['title']
        self.feed.link = json_feed['link']
        self.feed.description = json_feed['description']
        self.feed.last_update = parse(json_feed['published'])
        self.feed.save()


# TODO: rename
class RSSJsonItemParser:
    def __init__(self, feed: Feed):
        self.feed = feed

    def insert_news(self, json_items):
        news_items = [News.from_rss_json(self.feed.id, json_item) for json_item in json_items]
        News.objects.bulk_create(news_items)
