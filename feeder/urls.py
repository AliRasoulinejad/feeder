from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from feed.router import urls as news_urls

urlpatterns = [
    path("feedermin/", admin.site.urls),
    path("api/v1/users/", include("user.urls")),
    path("api/v1/", include(news_urls)),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
