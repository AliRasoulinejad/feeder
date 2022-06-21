from rest_framework.serializers import ModelSerializer

from feed.models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "user")
        read_only_fields = ("id", "user")

    def create(self, validated_data):
        validated_data["news_id"] = self.context["view"].kwargs["pk"]
        validated_data["user_id"] = self.context["request"].user.id
        return super().create(validated_data=validated_data)
