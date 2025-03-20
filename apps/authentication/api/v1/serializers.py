from apps.authentication.services import GoogleOAuthService

from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, token):
        user_info = GoogleOAuthService.verify_google_token(token)
        if not user_info:
            raise serializers.ValidationError("Invalid Google token")
        return token

    def create(self, validated_data):
        token = validated_data.get("token")
        user_info = GoogleOAuthService.verify_google_token(token)
        user, _ = GoogleOAuthService.get_or_create_user_from_google_info(user_info)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
