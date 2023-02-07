"""
Serialziers for camping APIs
"""
import datetime

from rest_framework import serializers

from core.models import Camping, CampingTag


def transform_str_to_datetime(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    return date_obj


class CampingTagSerialzier(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = CampingTag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class CampingSerializer(serializers.ModelSerializer):
    """Serializer for camping"""

    camping_tags = CampingTagSerialzier(many=True, required=False)

    class Meta:
        model = Camping
        fields = [
            "id",
            "title",
            "visited_dt",
            "review",
            "price",
            "camping_tags",
        ]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, instance=None):
        """
        tags 객체를 불러와서 camping object에 add
        """
        auth_user = self.context.get("request").user
        for camping_tag in tags:
            tag_obj, created = CampingTag.objects.get_or_create(user=auth_user, **camping_tag)
            instance.camping_tags.add(tag_obj)

    def create(self, validated_data):
        """Create a recipe"""
        camping_tags = validated_data.pop("camping_tags", [])  # [(TagObject1), (TagObject2), ...]
        camping = Camping.objects.create(**validated_data)

        self._get_or_create_tags(camping_tags, camping)

        return camping

    def update(self, instance, validated_data):
        """
        instance : <Camping Object>
        validated_data: request로 넘어온 dictionary 데이터
        """

        camping_tags = validated_data.pop("camping_tags", [])
        if camping_tags is not None:
            instance.camping_tags.clear()
            self._get_or_create_tags(camping_tags, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CampingDetailSerializer(CampingSerializer):
    """Serializer for camping detail view"""

    class Meta(CampingSerializer.Meta):
        fields = CampingSerializer.Meta.fields