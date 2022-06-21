from rest_framework.serializers import ModelSerializer

from feed.models import Feed


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = (
            "id",
            "title",
            "description",
            "link",
            "rss_url",
            "last_update",
            "get_absolute_url",
        )
        read_only_fields = fields
