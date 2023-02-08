from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.models import Recipe, RecipeTag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer, RecipeTagSerializer


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for the request"""
        if self.action == "list":
            return RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """recipe객체를 만들기전에 user 추가"""
        serializer.save(user=self.request.user)


class TagViewSet(ModelViewSet):
    serializer_class = RecipeTagSerializer
    queryset = RecipeTag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
