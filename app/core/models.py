"""
Database models.
"""

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for User"""

    def create_user(self, email, password=None, **extra_field):
        """create user"""

        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_field):
        """관리자 계정 생성 함수"""

        user = self.create_user(email, password, **extra_field)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Camping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campings")
    title = models.CharField(max_length=255)
    visited_dt = models.DateTimeField(default=timezone.now)
    review = models.TextField()
    price = models.PositiveIntegerField()

    update_dt = models.DateTimeField(auto_now=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    camping_tags = models.ManyToManyField("CampingTag")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-update_dt"]


class CampingTag(models.Model):
    """Tag object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)

    # slug = models.SlugField(max_length=255, allow_unicode=True, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'camping_tag'
        verbose_name_plural = _('Camping Tags')
        ordering = ['-name']


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_minutes = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    link = models.CharField(max_length=255, blank=True)

    recipe_tags = models.ManyToManyField("RecipeTag")

    update_dt = models.DateTimeField(auto_now=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-update_dt"]
        verbose_name = _("Recipe", )
        verbose_name_plural = _("Recipe")


class RecipeTag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, allow_unicode=True)

    update_dt = models.DateTimeField(auto_now=True)
    create_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["update_dt"]
