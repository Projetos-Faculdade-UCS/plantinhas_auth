from apps.authentication.services import GoogleOAuthService

from django.contrib.auth import authenticate
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
        if not user_info:
            raise serializers.ValidationError("Invalid Google token")
        user, _ = GoogleOAuthService.get_or_create_user_from_google_info(user_info)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "exp": refresh.access_token["exp"],
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            # Check if user is staff/admin if this endpoint is only for admins
            if not user.is_staff:
                raise serializers.ValidationError(
                    "User is not authorized to use this endpoint."
                )
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get("user")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "exp": refresh.access_token["exp"],
        }
