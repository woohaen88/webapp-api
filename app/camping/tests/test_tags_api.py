"""
Test for the tags API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APIClient

from camping.serializers import CampingTagSerialzier
from core.models import CampingTag

TAGS_URL = reverse("camping:camping-list")


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

class PrivateTagsAPITests(TestCase):
    """Test authenticated API request"""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        CampingTag.objects.create(user=self.user, name="Vegan", slug=slugify("Vegan", allow_unicode=True))
        CampingTag.objects.create(user=self.user, name="한글", slug=slugify("한글", allow_unicode=True))

        res = self.client.get(TAGS_URL)

        tags = CampingTag.objects.all()
        serializer = CampingTagSerialzier(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user"""
        user2 = create_user(email="user2@example.com")
        CampingTag.objects.create(user=user2, name="Fruitty", slug=slugify("Fruitty", allow_unicode=True))
        tag = CampingTag.objects.create(user=self.user, name="AfterTag", slug=slugify("AfterTag", allow_unicode=True))

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

