from django.db import models
from django.db.models import F


class NewsQuerySet(models.QuerySet):
    def unread_news_by_user_id(self, user_id):
        return self.exclude(
            users_read__user_id=user_id
        ).filter(
            feed__users_follow__user_id=user_id,
            feed__users_follow__created_at__lt=F("created_at")
        )


class News(models.Model):
    feed = models.ForeignKey('feed.Feed', on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField()
    author = models.EmailField(null=True, blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
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

    objects = NewsQuerySet.as_manager()

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        from rest_framework.reverse import reverse
        return reverse('news-viewset-detail', args=[self.id])

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

    def read_by_user_id(self, user_id: int) -> None:
        self.read_by.add(user_id)

    def bookmark_by_user_id(self, user_id: int) -> None:
        self.bookmarked_by.add(user_id)

    def remove_bookmark_by_user_id(self, user_id: int) -> None:
        self.bookmarked_by.remove(user_id)

    def favorite_by_user_id(self, user_id: int) -> None:
        self.favorite_by.add(user_id)

    def remove_favorite_by_user_id(self, user_id: int) -> None:
        self.favorite_by.remove(user_id)


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
