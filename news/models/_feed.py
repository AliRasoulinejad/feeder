from django.db import models


class UserFollowFeed(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='followed_feeds')
    feed = models.ForeignKey('news.Feed', on_delete=models.CASCADE, related_name='users_follow')


class Feed(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    rss_url = models.URLField(unique=True, db_index=True, help_text='unique url for scraping feed')
    last_update = models.DateTimeField(null=True, blank=True)
    followers = models.ManyToManyField(
        'user.User',
        related_name='feeds',
        through="news.UserFollowFeed"
    )

    def __str__(self):
        return f"{self.title}"
