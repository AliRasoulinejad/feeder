from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import User
from user.serializers import UserSignInSerializer
from user.serializers import UserSignUpSerializer


class SignInTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignInSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializer
