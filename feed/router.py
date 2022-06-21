from rest_framework.routers import DefaultRouter

from feed.viewsets import FeedViewSet, NewsViewSet

router = DefaultRouter()

router.register("feeds", FeedViewSet, basename="feed-viewset")
router.register("news", NewsViewSet, basename="news-viewset")

urls = router.urls
