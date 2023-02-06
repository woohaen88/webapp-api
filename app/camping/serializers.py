"""
Serialziers for camping APIs
"""
from django.utils.text import slugify
from rest_framework import serializers
from core.models import Camping, CampingTag



class CampingTagSerialzier(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = CampingTag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class CampingSerializer(serializers.ModelSerializer):
    """Serializer for camping"""

    tags = CampingTagSerialzier(many=True, required=False)

    class Meta:
        model = Camping
        fields = [
            "id",
            "title",
            "visited_dt",
            "review",
            "price",
            "tags",
        ]
        read_only_fields = ["id"]