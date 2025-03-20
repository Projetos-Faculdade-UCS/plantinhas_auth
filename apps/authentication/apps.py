from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"  # Changed from "authentication" to "apps.auth"
    verbose_name = "Authentication"
