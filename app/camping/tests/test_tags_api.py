"""
Test for the tags API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

TAGS_URL = reverse("camping:tag-list")


# def detail_url(tag_id):
#     """Create and return a tag detail url"""
#     return reverse("camping:tag-detail", args=[tag_id])


def create_user(**kwargs):
    defaults = dict(
        email="user@example.com",
        password="test123!@#",
        name="user",
    )
    defaults.update(kwargs)
    return get_user_model().objects.create_user(**defaults)


class PublicTagsApiTest(TestCase):
    """Test Unauthenticated API request"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for camping tag"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
