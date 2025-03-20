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

    def get_or_create_user(self, user_info):
        email = user_info.get("email")
        if not email:
            raise serializers.ValidationError("Email not provided by Google")

        # Try to find an existing user or create a new one
        user, _created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,  # Using email as username
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
            },
        )
        return user

    def create(self, validated_data):
        token = validated_data.get("token")
        user_info = GoogleOAuthService.verify_google_token(token)
        user = self.get_or_create_user(user_info)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
