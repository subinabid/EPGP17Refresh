"""URL configuration for EPGP project."""

from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from rest_framework.authtoken import views as drf_views  # type: ignore

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", drf_views.obtain_auth_token, name="api-token-auth"),
    path("api/", include("api.urls")),
]
