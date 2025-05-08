from apps.core.views import UserProfileView

from django.urls import path

from .views import JwksView

app_name = "core"
urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path(".well-known/jwks.json", JwksView.as_view(), name="jwks"),
]
