from django.contrib import admin

from feed.models import Feed, News, Comment


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    pass


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
