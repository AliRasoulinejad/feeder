from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from feed.models import News
from feed.serializers import NewsSerializer
from utils.permissions import DenyPermission


class NewsViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    model = News
    queryset = model.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            self.queryset = self.queryset.unread_news_by_user_id(self.request.user.id)
        return super().get_queryset()

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "create":
            permissions += [DenyPermission]
        return permissions

    @action(methods=['post'], detail=True)
    def read(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def comments(self, request, *args, **kwargs):
        from feed.serializers import CommentSerializer

        self.serializer_class = CommentSerializer
        return self.create(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def bookmarks(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(
            users_bookmark__user_id=request.user.id
        ).prefetch_related('users_bookmark')
        return self.list(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def bookmark(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.bookmark_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @bookmark.mapping.delete
    def delete_bookmark(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remove_bookmark_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def favorites(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(
            users_favorite__user_id=request.user.id
        ).prefetch_related('users_favorite')
        return self.list(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def favorite(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.favorite_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @favorite.mapping.delete
    def delete_favorite(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remove_favorite_by_user_id(request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
