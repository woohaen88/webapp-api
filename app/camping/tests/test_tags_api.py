"""
Test for the tags API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from camping.serializers import CampingTagSerialzier
from core.models import CampingTag

TAGS_URL = reverse("camping:campingtag-list")


def detail_url(tag_id):
    """Create and return a tag detail url"""
    return reverse("camping:campingtag-detail", args=[tag_id])


def create_user(**kwargs):
    defaults = dict(
        email="user@example.com",
        password="test123!@#",
        name="user",
    )
    defaults.update(kwargs)
    return get_user_model().objects.create_user(**defaults)


def create_tag(user, name):
    return CampingTag.objects.create(user=user, name=name, )


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
        CampingTag.objects.create(user=self.user, name="Vegan")
        CampingTag.objects.create(user=self.user, name="한글")

        res = self.client.get(TAGS_URL)

        tags = CampingTag.objects.all()
        serializer = CampingTagSerialzier(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user"""
        user2 = create_user(email="user2@example.com")
        CampingTag.objects.create(user=user2, name="Fruitty", )
        tag = CampingTag.objects.create(user=self.user, name="AfterTag", )

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        """Tag 업데이트"""
        tag = CampingTag.objects.create(user=self.user, name="tag1")
        payload = dict(name="new_tag1")
        url = detail_url(tag.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tag.refresh_from_db()
        self.assertEqual(tag.name, payload.get("name"))

    def test_delete_tag(self):
        """Tag 삭제"""
        tag = create_tag(user=self.user, name="tag1")
        url = detail_url(tag.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = CampingTag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
