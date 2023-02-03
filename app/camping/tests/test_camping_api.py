"""
test camping api
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Camping
from rest_framework import status
from rest_framework.test import APIClient

CAMPING_URL = reverse("camping:camping-list")

def create_camping(user, **params):
    """Create and return sample camping"""

    defaults = dict(
        title="DeepForest",
        visited_date="2022-12-03",
        review="Some review",
        price=50000,
    )

    defaults.update(params)

    camping = Camping.objects.create(user=user, **defaults)
    return camping

def create_user(**kwargs):
    """create and return user"""

    defaults = dict(email="email", password="test123!")
    defaults.update(kwargs)

    user = get_user_model().objects.create_user(**defaults)
    return user

class PublicCampingAPITests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CAMPING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

