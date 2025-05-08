from django.urls import path

from .views import GoogleAuthView
from .views import JwksView

urlpatterns = [
    path("google/", GoogleAuthView.as_view(), name="google-auth"),
    path(".well-known/jwks.json", JwksView.as_view(), name="jwks"),
]
