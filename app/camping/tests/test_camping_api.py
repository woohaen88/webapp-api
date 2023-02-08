"""
test camping api
"""
from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from camping.serializers import CampingSerializer
from core.models import Camping, CampingTag

CAMPING_URL = reverse("camping:camping-list")


def create_camping(user, **params):
    """Create and return sample camping"""

    defaults = dict(
        title="DeepForest",
        visited_dt="2022-12-03",
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


def detail_url(camping_id):
    """Create and return a recipe detail URL"""
    return reverse("camping:camping-detail", args=[camping_id])


class PublicCampingAPITests(TestCase):
    """Test unauthenticated API request."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CAMPING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API Request"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_campings(self):
        """Test: 인증된 유저에 대해서 모은 캠핑 리스트 조회"""
        create_camping(self.user)
        create_camping(self.user)

        res = self.client.get(CAMPING_URL)
        campings = Camping.objects.all()
        serialzier = CampingSerializer(campings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialzier.data)

    def test_recipe_list_ilmited_user(self):
        """Test list of campings is limited to authenticated user."""
        other_user = create_user(
            email="other@example.com",
            password="password123",
        )

        # create recipe
        create_camping(user=self.user)

        res = self.client.get(CAMPING_URL)

        campings = Camping.objects.filter(user=self.user)
        serializer = CampingSerializer(campings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_camping(self):
        """Test camping create and return camping"""

        payload = dict(
            title="DeepForest",
            visited_dt="2022-12-03",
            review="Some review",
            price=50000,
        )

        res = self.client.post(CAMPING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)  # 상태코드는 200이어야함
        camping = Camping.objects.get(id=res.data.get("id"))  # payload 각 속성별 value값이 object안에 있어야함
        for key, value in payload.items():
            if key == 'visited_dt':
                self.assertEqual(getattr(camping, key), datetime.strptime(payload.get('visited_dt'), '%Y-%m-%d'))
            else:
                self.assertEqual(getattr(camping, key), value)
        self.assertEqual(camping.user, self.user)  # user는 로그인한 유저와 같아야함
        self.assertEqual(camping.user, self.user)  # user는 로그인한 유저와 같아야함

    def test_partial_update(self):
        """Test partial update of a camping"""
        camping = create_camping(
            user=self.user,
            title="sample title"
        )

        payload = {"title": "New Title"}
        url = detail_url(camping.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        camping.refresh_from_db()

        self.assertEqual(camping.title, payload.get("title"))
        self.assertEqual(camping.user, self.user)

    def test_full_update(self):
        """Test Full update of a camping"""

        original_payload = dict(
            title="DeepForest",
            visited_dt="2022-12-03",
            review="Some review",
            price=50000,
        )
        camping = create_camping(
            user=self.user,
            **original_payload,
        )

        update_payload = dict(
            title="new DeepForest",
            visited_dt="2022-12-21",
            review="new Some review",
            price=10000,
        )

        url = detail_url(camping.id)
        res = self.client.put(url, update_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        camping.refresh_from_db()

        for key, value in update_payload.items():
            if key == 'visited_dt':
                self.assertEqual(getattr(camping, key), datetime.strptime(update_payload.get('visited_dt'), '%Y-%m-%d'))
            else:
                self.assertEqual(getattr(camping, key), value)
        self.assertEqual(camping.user, self.user)

    def test_delete_camping(self):
        """Test: 인증된 유저에 대해서 캠핑 삭제"""
        camping = create_camping(user=self.user)

        url = detail_url(camping.id)

        res = self.client.delete(url)
        self.assertFalse(Camping.objects.filter(id=camping.id).exists())
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_camping_other_users_camping_error(self):
        """Test: 다른사람이 캠핑을 생성하려하면 error"""
        new_user = create_user(
            email="user2@example",
            name="user2"
        )
        camping = create_camping(user=new_user)

        url = detail_url(camping.id)

        # 현재 인증되어 있는 유저는 self.user
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Camping.objects.filter(id=camping.id).exists())

    def test_camping_create_include_tag(self):
        """
        Test: 캠핑에 포스트 요청을 보낼 때 tag를 포함하여 보냄
        """

        CampingTag.objects.create(user=self.user, name="tag1", )
        CampingTag.objects.create(user=self.user, name="tag2", )

        payload = dict(
            title="DeepForest",
            visited_dt="2022-12-03",
            review="Some review",
            price=50000,
        )

        camping = create_camping(user=self.user, **payload)

        res = self.client.post(CAMPING_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for payload_Key, payload_value in payload.items():
            self.assertTrue(getattr(camping, payload_Key), payload_value)

        tag_names = ["tag1", "tag2"]
        for camping_tags, tag_name in zip(camping.camping_tags.all(), tag_names):
            self.assertEqual(camping_tags.name, tag_name)

    def test_create_tag_on_update(self):
        """
        camping object를 만들고 태그 업데이트
        """
        camping = create_camping(user=self.user)

        payload = dict(camping_tags=[dict(name="lunch")])

        url = detail_url(camping.id)

        res = self.client.patch(url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        tag = CampingTag.objects.get(user=self.user, name="lunch")
        self.assertIn(tag, CampingTag.objects.all())

    def test_update_camping_assign_tag(self):
        """
        Test assign an existing tag when updating a camping.
        """
        tag_breakfast = CampingTag.objects.create(user=self.user, name="breakfast")
        camping = create_camping(user=self.user)
        camping.camping_tags.add(tag_breakfast)

        # create another tag
        tag_lunch = CampingTag.objects.create(user=self.user, name="lunch")

        url = detail_url(camping.id)
        payload = {"camping_tags": [{"name": "lunch"}]}

        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_clear_camping_tags(self):
        """Test clearing a recipes tags."""
        dessert_tag = CampingTag.objects.create(user=self.user, name="Dessert")
        camping = create_camping(user=self.user)
        camping.camping_tags.add(dessert_tag)

        payload = dict(camping_tags=[])

        url = detail_url(camping.id)
        res = self.client.patch(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(camping.camping_tags.count(), 0)
