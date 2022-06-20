from rest_framework.serializers import ModelSerializer, SerializerMethodField

from feed.models import News
from feed.serializers.comment_serializer import CommentSerializer


class NewsSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    total_unread_count = SerializerMethodField()

    class Meta:
        model = News
        fields = (
            "id", "feed", "title", "description", "link", "author", "created_at", "published_at",
            "get_absolute_url", "comments", "total_unread_count"
        )
        read_only_fields = fields

    def get_total_unread_count(self, obj):
        return self.context['view'].queryset.count()
