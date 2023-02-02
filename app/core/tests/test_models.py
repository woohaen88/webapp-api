"""
Test for models
"""

from django.test import TestCase

from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_without_email_raise_error(self):
        """email이 없으면 에러"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", password="password123")

    def test_create_superuser(self):
        """관리자 계정 생성"""
        email = "user@example.com"
        password = "password"
        user = get_user_model().objects.create_superuser(email, password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
