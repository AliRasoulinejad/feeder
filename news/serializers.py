from rest_framework.serializers import ModelSerializer

from news.models import Feed


class FeedSerializer(ModelSerializer):

    class Meta:
        model = Feed
        fields = ("title", "description", "link", "rss_url", "last_update", "url",)
        read_only_fields = fields