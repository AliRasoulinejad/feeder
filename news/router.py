from rest_framework.routers import DefaultRouter

from news.viewsets import FeedViewSet

router = DefaultRouter()

router.register("feeds", FeedViewSet, basename='feed-viewset')

urls = router.urls
