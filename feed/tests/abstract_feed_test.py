from datetime import datetime

from feed.models import Feed
from utils.tests import AbstractFeederTest


class AbstractFeedTest(AbstractFeederTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.sample_feed = Feed.objects.create(
            title="Sample Feed - Favorite RSS Related Software & Resources",
            description="Take a look at some of FeedForAll's favorite software and resources for "
            "learning more about RSS.",
            link="https://www.feedforall.com",
            rss_url="https://www.feedforall.com/sample-feed.xml",
            last_update=datetime(2004, 10, 26, 14, 6, 44),
        )
