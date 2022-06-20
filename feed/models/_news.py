from django.db import models


class News(models.Model):
    feed = models.ForeignKey('feed.Feed', on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField()
    author = models.EmailField()
    published_at = models.DateTimeField()
    read_by = models.ManyToManyField(
        'user.User',
        related_name='reads_news',
        through="feed.UserReadNews"
    )
    favorite_by = models.ManyToManyField(
        'user.User',
        related_name='favorites',
        through="feed.UserFavoriteNews"
    )

    bookmarked_by = models.ManyToManyField(
        'user.User',
        related_name='bookmarks',
        through="feed.UserBookmarkNews"
    )

    def __str__(self):
        return f"{self.title}"

    @classmethod
    def from_rss_json(cls, feed_id, json_item):
        title = json_item.get("title", "")
        link = json_item.get("link", "")
        description = json_item.get("description", "")
        author = json_item.get("author")
        published_at = json_item.get("pubDate")
        return cls(
            feed_id=feed_id,
            title=title, link=link, description=description, author=author,
            published_at=published_at,
        )


class UserReadNews(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='read_news')
    news = models.ForeignKey('feed.News', on_delete=models.CASCADE, related_name='users_read')

    class Meta:
        unique_together = ("user", "news")


class UserFavoriteNews(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='favorites_news')
    news = models.ForeignKey('feed.News', on_delete=models.CASCADE, related_name='users_favorite')

    class Meta:
        unique_together = ("user", "news")


class UserBookmarkNews(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='bookmarked_news')
    news = models.ForeignKey('feed.News', on_delete=models.CASCADE, related_name='users_bookmark')

    class Meta:
        unique_together = ("user", "news")
