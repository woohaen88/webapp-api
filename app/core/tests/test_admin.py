"""
Tests for the Django admin modification
"""
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


def create_user(**kwargs):
    defaults = {"email": "user@example.com", "password": "test123!@#", "name": "user"}
    defaults.update(kwargs)

    user = get_user_model().objects.create_user(**defaults)
    return user


class AdminSiteTests(TestCase):
    """Django admin 테스트"""

    def setUp(self) -> None:
        """init setting"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email="admin@admin.com")

        # 생성한 유저로 로그인
        self.client.force_login(self.admin_user)
        self.user = create_user()

    def test_users_list(self) -> None:
        """admin 페이지에 user목록 check"""

        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_page(self) -> None:
        """admin 페이지 수정"""

        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.user.name)

    def test_create_user_page(self):
        """유저 생성 테스트"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
