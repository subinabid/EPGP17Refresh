"""API URL Configuration"""

from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path("user/", views.userinfo, name="user-info"),
    path("users/", views.ListUsers.as_view(), name="user-list"),
    path("users/<int:pk>", views.get_user_queryset, name="user-detail"),
    path("users/create/", views.create_user, name="create-user"),
    path("users/update/", views.update_user_self, name="update-user"),
    path("users/update/<int:pk>", views.update_user_admin, name="update-user"),
    path("users/batch", views.batch_info, name="batch-info"),
    path("users/social", views.get_social_links, name="social-links"),
    path("electives/", views.list_electives, name="elective-list"),
    path("electives/<int:pk>", views.elective_detail, name="elective-detail"),
    path("electives/<int:pk>/takers", views.elective_takers, name="elective-takers"),
    path("electives/enrolled/", views.enrolled_elective, name="elective-enrolled"),
    path("electives/enroll/<int:pk>", views.enroll_elective, name="elective-enroll"),
]
