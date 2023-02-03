"""
URL mapping for camping
"""

from rest_framework.routers import DefaultRouter
from camping import views
from django.urls import path, include

router = DefaultRouter()
router.register("campings", views.CampingViewSet)

app_name = 'camping'

urlpatterns = [
    path("", include(router.urls))
]