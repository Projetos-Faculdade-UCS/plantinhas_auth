from django.urls import path

from .views import GoogleAuthView
from .views import UserLoginView

urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="google-auth"),
    path("login/", UserLoginView.as_view(), name="admin-login"),
]
