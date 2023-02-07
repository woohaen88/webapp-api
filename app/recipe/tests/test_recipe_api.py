from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def create_user(email="user@example.com", password="test123!@#", name="user"):
    return get_user_model().objects.create_user(email=email, password=password, name=name)

RECIPE_URL = reverse("router:aa")

class PublicRecipeAPIsTest(TestCase):
    """권한 없는 유저일 경우 권한 없음 표시"""
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()

    def test_public_request_return_error(self):
        """권한 없는 유저일 경우 권한 없음 표시"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)