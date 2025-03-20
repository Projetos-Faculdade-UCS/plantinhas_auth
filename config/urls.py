from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("auth/", include("apps.authentication.urls")),  # Added trailing slash
]
