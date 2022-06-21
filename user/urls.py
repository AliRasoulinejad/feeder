from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import (
    SignInTokenPairView,
    SignUpView,
)

urlpatterns = [
    path("sign-in/", SignInTokenPairView.as_view(), name="signin-token"),
    path("sign-in/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("sign-up/", SignUpView.as_view(), name="user-signup"),
]
