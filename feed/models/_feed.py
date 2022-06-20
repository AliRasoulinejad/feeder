from django.db import models


class UserFollowFeed(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='followed_feeds')
    feed = models.ForeignKey('feed.Feed', on_delete=models.CASCADE, related_name='users_follow')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "feed")


class Feed(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    rss_url = models.URLField(unique=True, db_index=True, help_text='unique url for scraping feed')
    last_update = models.DateTimeField(null=True, blank=True)
    followers = models.ManyToManyField(
        'user.User',
        related_name='feeds',
        through="feed.UserFollowFeed"
    )

    def __str__(self):
        return f"{self.title}"

    def url(self):
        from rest_framework.reverse import reverse
        return reverse('feed-viewset-detail', args=[self.id])

    def follow_by_user_id(self, user_id: int) -> None:
        self.followers.add(user_id)

    def remove_follow_by_user_id(self, user_id: int) -> None:
        self.followers.remove(user_id)
