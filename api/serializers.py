from django.contrib.auth.models import User, Group  # type: ignore
from .models import BatchInfo, SocialLinks, Employment
from rest_framework import serializers  # type: ignore


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
        ]


class BatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchInfo
        fields = "__all__"
        read_only_fields = ["user"]


class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = "__all__"
        read_only_fields = ["user"]


class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = "__all__"
        read_only_fields = ["user"]
