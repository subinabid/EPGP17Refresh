"""API URL Configuration"""

from django.urls import path  # type: ignore
from rest_framework.schemas import get_schema_view  # type: ignore
from rest_framework.renderers import JSONOpenAPIRenderer  # type: ignore
from . import views

schema_view = get_schema_view(
    title="EPGP API",
    description="API for EPGP data access",
    version="1.0.0",
    renderer_classes=[JSONOpenAPIRenderer],
)


urlpatterns = [
    path("schema.json", schema_view, name="openapi-schema"),
    path("users/", views.userinfo, name="user-info"),
    path("users/<int:pk>", views.userinfo, name="user-info-id"),
    path("user/batch", views.batch_info, name="batch-info"),
    path("user/social", views.social_links, name="social-links"),
    path("user/update/", views.update_user_self, name="update-user"),
    path("user/change-pwd/", views.change_password, name="change-password"),
    path("users/", views.ListUsers.as_view(), name="user-list"),
    path("users/create/", views.create_user, name="create-user"),
    path("users/<int:pk>/update", views.update_user_admin, name="update-user"),
    path("users/<int:pk>/batch", views.batch_info_by_id, name="batch-info"),
    path("users/<int:pk>/social", views.social_links_by_id, name="batch-info"),
    path("users/<int:pk>/electives", views.electives_by_user, name="electives-by-user"),
    path("electives/", views.list_electives_for_user, name="elective-list"),
    path("electives/all", views.list_all_electives, name="all_elective-list"),
    path("electives/<int:pk>", views.elective_detail, name="elective-detail"),
    path("electives/<int:pk>/takers", views.elective_takers, name="elective-takers"),
    path("electives/enrolled/", views.enrolled_elective, name="elective-enrolled"),
    path("electives/enroll/<int:pk>", views.enroll_elective, name="elective-enroll"),
    path("centres", views.StudyCentresView.as_view()),
    path("centres/<int:id>/poc/", views.StudyCentrePOCView.as_view()),
]
