"""
Serialzier for Recipe API
"""

from rest_framework import serializers

from core.models import Recipe, RecipeTag
from user.serializers import UserSerialzier


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    user = UserSerialzier(read_only=True)
    recipe_tags = RecipeTagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "user", "title", "time_minutes", "price", "link", "update_dt", "create_dt", "recipe_tags"]
        read_only_fields = ["id", "update_dt", "create_dt", "user"]

    def _get_or_create_instance_tags(self, recipe_tags, instance=None):
        auth_user = self.context.get("request").user
        for recipe_tag in recipe_tags:
            tag_obj, is_created = RecipeTag.objects.get_or_create(user=auth_user, **recipe_tag)
            if getattr(instance, "recipe_tags", False):
                instance.recipe_tags.add(tag_obj)

    def create(self, validated_data):
        recipe_tags = validated_data.pop("recipe_tags", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_instance_tags(recipe_tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        recipe_tags = validated_data.pop("recipe_tags", [])
        if recipe_tags is not None:
            instance.recipe_tags.clear()
            self._get_or_create_instance_tags(recipe_tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
