"""
Views for the camping APIs
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from camping.serializers import CampingSerializer, CampingTagSerialzier
from core.models import Camping, CampingTag
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CampingViewSet(viewsets.ModelViewSet):
    """View for mange camping APIs"""

    serializer_class = CampingSerializer
    queryset = Camping.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve camping for authenticated user."""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new camping"""
        serializer.save(user=self.request.user)


class TagViewSet(ListModelMixin, GenericViewSet):
    """manage tags in the database"""

    serializer_class = CampingTagSerialzier
    queryset = CampingTag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")