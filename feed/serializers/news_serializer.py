from rest_framework.serializers import ModelSerializer

from feed.models import News


class NewsSerializer(ModelSerializer):

    class Meta:
        model = News
        fields = (
            "id", "feed", "title", "description", "link", "author", "created_at", "published_at",
            "get_absolute_url"
        )
        read_only_fields = fields
