from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, RecipeTag


def create_user(email="user@example.com", password="test123!@#", name="user"):
    return get_user_model().objects.create_user(email=email, password=password, name=name)


def create_recipe(user,
                  title="sample title",
                  description="some description",
                  time_minutes=5,
                  price=10000,
                  link="http://example.com", **kwargs):
    payload = dict(
        user=user,
        title=title,
        description=description,
        time_minutes=time_minutes,
        price=price,
        link=link,
        **kwargs,
    )
    recipe = Recipe.objects.create(**payload)
    return recipe


RECIPE_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    return reverse("recipe:recipe-detail", args=[recipe_id])


class PublicRecipeAPIsTest(TestCase):
    """권한 없는 유저일 경우 권한 없음 표시"""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()

    def test_public_request_return_error(self):
        """권한 없는 유저일 경우 권한 없음 표시"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPIsTest(TestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.client.force_login(self.user)

    def test_get_all_recipe_list(self):
        """모든 레서피 조회"""
        create_recipe(self.user, title="title1")
        create_recipe(self.user, title="title2")

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(Recipe.objects.filter(user=self.user).count(), 2)

    def test_get_limited_user(self):
        """특정 유저만 레서피 조회"""
        user1 = create_user(email="user1@example.com")
        create_recipe(user1)

        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(Recipe.objects.filter(user=self.user).count(), 0)

    def test_create_recipe(self):
        """레서피 생성"""
        payload = dict(
            title="sample title",
            description="some description",
            time_minutes=5,
            price=10000,
            link="http://example.com"
        )
        recipe = create_recipe(self.user, **payload)
        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for recipe_key, recipe_value in payload.items():
            self.assertEqual(getattr(recipe, recipe_key), recipe_value)

    def test_full_update_recipe(self):
        """전체 레서피 업데이트"""
        recipe = create_recipe(self.user)

        payload = dict(
            title="new title",
            description="new description",
            time_minutes=15,
            price=20000,
            link="http://new_example.com"
        )

        url = detail_url(recipe.id)
        res = self.client.put(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        for recipe_key, recipe_value in payload.items():
            self.assertEqual(getattr(recipe, recipe_key), recipe_value)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        """부분 레서피 업데이트"""
        recipe = create_recipe(self.user)
        payload = dict(title="new title")

        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload.get("title"))

    def test_get_detail_recipe(self):
        """디테일 레서피 조회"""
        recipe = create_recipe(self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        attrs = ["title", "description", "time_minutes", "price", "link"]

        for attr in attrs:
            value = getattr(recipe, attr, None)
            self.assertIsNotNone(value)

    def test_delete_recipe(self):
        """특정 레서피 삭제"""
        recipe = create_recipe(self.user)

        url = detail_url(recipe.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Recipe.objects.filter(user=self.user).exists()
        self.assertFalse(exists)

    def test_create_recipe_with_tags(self) -> None:
        """tag를 포함하여 Recipe 생성"""
        payload = dict(
            title="sample title",
            description="some description",
            time_minutes=5,
            price=10000,
            link="http://example.com",
            recipe_tags=[dict(name="tag1"), dict(name="tag2")]
        )

        res = self.client.post(RECIPE_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(user=self.user)

        for key, value in payload.items():
            if key == "recipe_tags":
                self.assertEqual(recipe.recipe_tags.count(), 2)
            else:
                self.assertEqual(getattr(recipe, key), value)

    def test_create_recipe_with_include_existing_tags(self) -> None:
        """tag를 포함하여 Recipe 생성(기존에 tag가 있는 것 포함)"""
        tag1 = RecipeTag.objects.create(user=self.user, name="tag1")
        payload = dict(
            title="sample title",
            description="some description",
            time_minutes=5,
            price=10000,
            link="http://example.com",
            recipe_tags=[dict(name="tag1"), dict(name="tag2")]
        )
        res = self.client.post(RECIPE_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.recipe_tags.count(), 2)
        self.assertIn(tag1, recipe.recipe_tags.all())
        for tag in payload["recipe_tags"]:
            exists = recipe.recipe_tags.filter(
                user=self.user,
                name=tag["name"]
            ).exists()
            self.assertTrue(exists)

    def test_update_recipe_with_tag(self) -> None:
        """tag를 포함하여 생성된 Recipe중 partial update"""
        recipe = create_recipe(user=self.user)

        payload = {"recipe_tags": [{"name": "Lunch"}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")
        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag = RecipeTag.objects.get(user=self.user, name="Lunch")
        self.assertIn(tag, recipe.recipe_tags.all())

    def test_full_update_recipe_with_tag(self) -> None:
        """tag를 포함하여 생성된 Recipe 전체 업데이트"""
        pass

    def test_clear_tag_in_recipe(self) -> None:
        """생성된 Recipe중 tag clear"""
        tag = RecipeTag.objects.create(user=self.user, name="Dessert")
        recipe = create_recipe(user=self.user)
        recipe.recipe_tags.add(tag)

        payload = {"recipe_tags": []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format="json")
        recipe.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.recipe_tags.count(), 0)
