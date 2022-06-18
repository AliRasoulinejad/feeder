from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    link = models.URLField()
    author = models.EmailField()
    published_at = models.DateTimeField()
    read_by = models.ManyToManyField(
        'user.User',
        related_name='reads_news',
        through="news.UserReadNews"
    )
    favorite_by = models.ManyToManyField(
        'user.User',
        related_name='favorites',
        through="news.UserFavoriteNews"
    )

    bookmarked_by = models.ManyToManyField(
        'user.User',
        related_name='bookmarks',
        through="news.UserBookmarkNews"
    )

    def __str__(self):
        return f"{self.title}"


class UserReadNews(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='read_news')
    news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='users_read')


class UserFavoriteNews(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='favorites_news')
    news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='users_favorite')


class UserBookmarkNews(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='bookmarked_news')
    news = models.ForeignKey('news.News', on_delete=models.CASCADE, related_name='users_bookmark')
