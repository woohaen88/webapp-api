"""
URL mapping for camping
"""

from rest_framework.routers import DefaultRouter
from camping import views
from django.urls import path, include

router = DefaultRouter()
router.register("campings", views.CampingViewSet)
router.register("tags", views.TagViewSet)

app_name = 'camping'
print(router.urls)

urlpatterns = [
    path("", include(router.urls))
]