from django.contrib.auth import get_user_model

from core.models import RecipeTag


def create_user(email="user@example.com", password="test123!@#", name="user"):
    kwargs = dict(
        email=email,
        password=password,
        name=name,
    )
    return get_user_model().objects.create_user(**kwargs)


def create_recipe_tag(user, name="tag1"):
    kwargs = dict(
        name=name,
    )
    return RecipeTag.objects.create(user=user, **kwargs)
