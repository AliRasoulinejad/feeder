from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from feed.models import Feed
from feed.serializers import FeedSerializer


class FeedViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    model = Feed
    queryset = model.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False)
    def followed(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(followers=request.user)
        return self.list(request, *args, **kwargs)

    @action(methods=["post"], detail=True)
    def follow(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.follow_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @follow.mapping.delete
    def delete_follow(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remove_follow_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
