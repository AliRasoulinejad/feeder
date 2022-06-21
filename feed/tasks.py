from feed.models import Feed
from feeder.celery import app as celery_app, BaseTaskWithRetry


@celery_app.task
def update_feeds_daily_task():
    for feed in Feed.objects.all().iterator(chunk_size=100):
        update_feed.delay(feed_id=feed.id)


@celery_app.task(bind=True, base=BaseTaskWithRetry)
def update_feed(bind, *, feed_id: int, **kwargs):
    from feed.scraper import FeedUpdater

    feed = Feed.objects.get(id=feed_id)
    FeedUpdater(feed).update()
