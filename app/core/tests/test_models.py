"""
Test for models
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify

from core import models
from utils.functools import create_user


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
        name = email.split("@")[0]
        user = get_user_model().objects.create_superuser(email, password, name=name)
        self.assertTrue(user.is_staff)
        self.assertEqual(name, user.name)
        self.assertTrue(user.is_superuser)

    ################################
    ###    CAMPING MODEL TEST    ###
    ################################
    def test_create_camping(self):
        """Test: Create Camping"""

        user = create_user()
        camping = models.Camping.objects.create(
            user=user,
            title="DeepForest",
            visited_dt="2022-12-03",
            review="Some review",
            price=50000,
        )
        self.assertEqual(str(camping), camping.title)

    ###########################################
    #####         TAG MODEL TEST          #####
    ###########################################
    def test_create_camping_tag(self):
        """Test: Create Camping Tag"""

        user = create_user()
        camping = models.CampingTag.objects.create(
            user=user,
            name="tag",
            # slug=slugify("tag", allow_unicode=True),
        )

        self.assertEqual(str(camping), camping.name)

    def test_create_recipe(self):
        """Recipe model create"""
        user = create_user()
        recipe = models.Recipe.objects.create(
            user=user,
            title="some_title",
            description="some description",
            time_minutes=5,
            price=10,
            link="http://example.com",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_recipetag(self):
        """recipetag create"""
        user = create_user()
        recipe_tag = models.RecipeTag.objects.create(
            user=user,
            name="name",
            slug=slugify("name", allow_unicode=True)
        )
        self.assertEqual(str(recipe_tag), recipe_tag.name)
