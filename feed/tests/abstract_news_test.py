from datetime import datetime

from feed.models import News
from feed.tests.abstract_feed_test import AbstractFeedTest


class AbstractNewsTest(AbstractFeedTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sample_news = News.objects.create(
            feed_id=cls.sample_feed.id,
            title="Recommended Desktop Feed Reader Software",
            description="""<b>FeedDemon</b> enables you to quickly read and gather information
from hundreds of web sites - without having to visit them. Don't waste any more time
checking your favorite web sites for updates. Instead, use FeedDemon and make them
come to you. <br> More <a
href="http://store.esellerate.net/a.asp?c=1_SKU5139890208_AFL403073819">FeedDemon
Information</a>""",
            link="https://www.feedforall.com/feedforall-partners.htm",
            author="",
            published_at=datetime(2004, 10, 26, 14, 3, 25),
        )
