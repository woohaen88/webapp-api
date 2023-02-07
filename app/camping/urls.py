"""
URL mapping for camping
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from camping import views

router = DefaultRouter()
router.register("campings", views.CampingViewSet)
router.register("tags", views.TagViewSet)

app_name = 'camping'

urlpatterns = [
    path("", include(router.urls))
]
