from django.contrib.auth.models import User, Group  # type: ignore
from .models import (
    BatchInfo,
    SocialLinks,
    Employment,
    Professor,
    Elective,
    ElectiveOffering,
    ElectiveEnrollment,
)
from rest_framework import serializers  # type: ignore


######################################################################
## SocialLinks, BatchInfo, Employment serializers
######################################################################


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


######################################################################
## user related serializers
######################################################################


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class DetailUserSerializer(serializers.ModelSerializer):
    batch_info = BatchInfoSerializer(read_only=True)
    social_links = SocialLinksSerializer()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "batch_info",
            "social_links",
        ]


################################################################################
## Elective related serializers
################################################################################


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["salutation", "name", "area"]


class ElectiveSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)

    class Meta:
        model = Elective
        fields = "__all__"


class ElectiveDetailSerializer(serializers.ModelSerializer):
    course = ElectiveSerializer(read_only=True)

    class Meta:
        model = ElectiveOffering
        fields = "__all__"


class ElectiveOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectiveOffering
        fields = "__all__"


class ElectiveOfferingSmallSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = ElectiveOffering
        fields = ["id", "course", "track", "section"]
        read_only_fields = ["id"]


class ElectiveEnrollmentSerializer(serializers.ModelSerializer):
    elective_offering = ElectiveOfferingSmallSerializer(read_only=True)

    class Meta:
        model = ElectiveEnrollment
        fields = ["id", "elective_offering"]
        read_only_fields = ["id"]
