"""
View for the user API
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import UserSerialzier, UserAuthTokenSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerialzier


class CreateTokenView(ObtainAuthToken):
    """유저에 대해 유효한 토큰 생성"""

    serializer_class = UserAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerialzier
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
