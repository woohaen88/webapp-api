"""
Test for the user APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

USER_CREATE_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**kwargs):
    """Create and Return a user."""
    defaults = dict(email="user@example.com", password="testpassword123", name="user")
    defaults.update(kwargs)
    return get_user_model().objects.create_user(**defaults)


class PublicUserAPITests(TestCase):
    """Test the public features of the user api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self):
        """Test create user"""
        payload = dict(
            email="test@example.com",
            password="testexample",
            name="test",
        )

        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user_list = get_user_model().objects.filter(email=payload.get("email"))
        self.assertTrue(user_list.exists())

        user = user_list.first()

        self.assertTrue(user.check_password(payload.get("password")))
        self.assertNotIn("password", res.data)

        self.assertEqual(user.name, payload.get("name"))

    def test_user_with_email_exists_erorr(self):
        """Test error if user with email exists."""
        payload = dict(
            email="test@example.com",
            password="testexample",
            name="test",
        )
        create_user(**payload)

        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload.get("email")).exists()
        self.assertTrue(user_exists)

    def test_password_too_short(self):
        """Test password too short"""
        payload = dict(
            email="test@example.com",
            password="abc",
            name="test",
        )
        res = self.client.post(USER_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(email=payload.get("email")).exists())

    ####################################################################################################

    ## Token Test
    def test_create_token_for_user(self):
        """Test generates token for valid credentials"""

        # defaults = dict(email="user@example.com", password="testpassword123", name="user")
        create_user()

        payload = dict(
            email="user@example.com",
            password="testpassword123",
        )
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """invalid credentials가 요청되면 error"""
        create_user()
        payload = dict(password="abc")
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_blank_password(self):
        """empty credentials가 요청되면 error"""
        create_user()
        payload = dict(password="")
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """인증되지 않은 user가 token을 요청하면 error"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
