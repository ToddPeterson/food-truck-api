from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings

from user import serializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    permission_classes = (AllowAny,)
    serializer_class = serializers.AuthTokenSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES
