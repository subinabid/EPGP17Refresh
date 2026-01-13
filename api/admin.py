"""Admin configuration for the API app"""

from django.contrib import admin  # type: ignore
from .models import (
    StudyCenter,
    StudyCentrePOC,
    BatchInfo,
    SocialLinks,
    Employment,
    Professor,
    Elective,
    ElectiveOffering,
    ElectiveEnrollment,
)


@admin.register(StudyCenter)
class StudyCenterAdmin(admin.ModelAdmin):
    list_display = ("state", "city", "location")


@admin.register(StudyCentrePOC)
class StudyCenterPOCAdmin(admin.ModelAdmin):
    list_display = ("centre", "person", "number")


@admin.register(BatchInfo)
class BatchInfoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "epgp_batch",
        "epgp_group",
        "roll_number",
        "studyCenter",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    search_fields = ("user__username", "user__email")


@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ("user", "personalEmail", "phone")
    search_fields = ("user__username", "personalEmail", "phone")


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ("user", "employer", "position", "start_date", "end_date")
    search_fields = ("user__username", "employer", "position")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("salutation", "name", "area", "email", "phone")
    search_fields = ("name", "email", "area")


@admin.register(Elective)
class ElectiveAdmin(admin.ModelAdmin):
    list_display = ("area", "course_code", "course_name", "instructor", "credits")
    search_fields = ("area", "course_code", "course_name", "instructor")


@admin.register(ElectiveOffering)
class ElectiveOfferingAdmin(admin.ModelAdmin):
    list_display = ("epgp_batch", "term", "course", "track", "section")
    search_fields = ("course__course_code", "course__course_name")


@admin.register(ElectiveEnrollment)
class ElectiveEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "elective_offering")
    search_fields = (
        "user__username",
        "elective_offering__course__course_code",
        "elective_offering__course__course_name",
    )


admin.site.site_title = "EPGP"
admin.site.site_header = "EPGP Admin"
