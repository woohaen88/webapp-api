from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import RecipeTag
from utils.functools import create_user, create_recipe_tag

TAG_URL = reverse("recipe:recipetag-list")


def detail_url(recipe_tag_id):
    return reverse("recipe:recipetag-detail", args=[recipe_tag_id])


class PublicTagApiTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()

    def test_request_unauthenticated_user_return_error(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPiTests(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_all_tags(self) -> None:
        """
        인증된 유저에 대해 전체 태그 불러오기
        """
        create_recipe_tag(self.user)
        create_recipe_tag(self.user)

        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe_tag = RecipeTag.objects.filter(user=self.user)
        self.assertEqual(recipe_tag.count(), 2)

    def test_get_tag_limited_user(self) -> None:
        """
        작성자가 작성한 태그만 보이는지 테스트
        """
        user1 = create_user("user1@example.com")
        create_recipe_tag(user=user1)

        recipe_tag = RecipeTag.objects.filter(user=self.user)
        self.assertEqual(recipe_tag.count(), 0)

    def test_create_tag(self) -> None:
        """
        인증된 유저가 태그를 생성
        """
        payload = dict(name="tag1")
        res = self.client.post(TAG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe_tag = RecipeTag.objects.filter(user=self.user).first()
        self.assertEqual(recipe_tag.name, payload.get("name"))

    def test_update_partial_tag(self) -> None:
        """
        인증된 유저가 태그를 업데이트
        """
        recipe_tag = create_recipe_tag(self.user, name="tag1")
        payload = dict(name="new tag")

        url = detail_url(recipe_tag.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe_tag.refresh_from_db()
        self.assertEqual(recipe_tag.name, payload.get("name"))

    def test_delete_tag(self) -> None:
        """
        인증된 유저가 태그를 삭제
        """
        recipe_tag = create_recipe_tag(self.user, name="tag1")

        url = detail_url(recipe_tag.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = RecipeTag.objects.filter(user=self.user).exists()
        self.assertFalse(exists)
