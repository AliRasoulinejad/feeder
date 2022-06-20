from django.contrib import admin

from news.models import Feed, News


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    pass


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass
