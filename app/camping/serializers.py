"""
Serialziers for camping APIs
"""
from rest_framework import serializers
from core.models import Camping

class CampingSerializer(serializers.ModelSerializer):
    """Serializer for camping"""

    class Meta:
        model = Camping
        fields = [
            "id",
            "title",
            "visited_dt",
            "review",
            "price",
        ]
        read_only_fields = ["id"]

    # def create(self, validated_data):
    #     """Create a camping"""
    #     auth_user = self.context.get("request").user
