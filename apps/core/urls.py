from apps.core.views import UserProfileView

from django.urls import path

app_name = "core"
urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
]
