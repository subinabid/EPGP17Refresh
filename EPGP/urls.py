"""URL configuration for EPGP project."""

from django.contrib import admin  # type: ignore
from django.urls import path, include  # type: ignore
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Generates access/refresh tokens
    TokenRefreshView,  # Generates a new access token using a refresh token
    TokenVerifyView,  # Verifies a token's validity
)
from rest_framework.authtoken import views as drf_views  # type: ignore

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", drf_views.obtain_auth_token, name="api-token-auth"),
    path("api/", include("api.urls")),
]
