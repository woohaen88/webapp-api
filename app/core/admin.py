"""
Django admin customizations
"""
from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    """Define the admin page for users."""

    ordering = ["id"]
    list_display = ("email", "name",)
    fieldsets = (
        (_("INFO"), {
            "fields": ("email", "name", "password",)
        },),
        (_("PERMISSIONS"), {
            "fields": ("is_active", "is_staff", "is_superuser",)
        },),
        (_("IMPORTANT DATES"), {
            "fields": ("last_login",)
        },),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (_("ADD FIELDS"),
         {
             "classes": ("wide",),
            "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

@admin.register(models.CampingTag)
class CampingTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",),}