from django.db import models


class Comment(models.Model):
    news = models.ForeignKey('feed.News', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
