from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import cast

from django.conf import settings
from django.contrib.auth.models import User

from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleOAuthService:
    # Google OAuth Client IDs from settings
    WEB_CLIENT_ID = settings.GOOGLE_OAUTH.get("WEB_CLIENT_ID")
    # Add more client IDs if needed
    ALLOWED_CLIENT_IDS = [WEB_CLIENT_ID]

    @classmethod
    def verify_google_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a Google OAuth2 JWT token and extract user information.

        Args:
            token: The JWT token received from the client

        Returns:
            Dictionary with user information or None if verification fails
        """
        try:
            print("Validating token")
            # Verify the token
            idinfo: dict[str, Any] = id_token.verify_oauth2_token(
                token,
                requests.Request(),  # cls.WEB_CLIENT_ID
            )
            print(idinfo)

            # If email is not verified, throw exception
            if not idinfo.get("email_verified", False):
                raise NotVerifiedEmailError("Email not verified")

            # Return relevant user information
            return {
                "user_id": idinfo["sub"],
                "email": idinfo.get("email"),
                "name": idinfo.get("name"),
                "picture": idinfo.get("picture"),
                "given_name": idinfo.get("given_name"),
                "family_name": idinfo.get("family_name"),
                "locale": idinfo.get("locale"),
                "raw_idinfo": idinfo,  # Include full payload for custom needs
            }

        except ValueError as e:
            # Invalid token
            print(f"Token validation error: {e}")
            return None

    @classmethod
    def get_or_create_user_from_google_info(
        cls, user_info: Dict[str, Any]
    ) -> Tuple[User, bool]:
        """
        Get or create a user from Google OAuth information.

        Args:
            user_info: Dictionary with user information from Google OAuth

        Returns:
            Tuple of (User object, created)
        """
        email = user_info.get("email")
        if not email:
            raise ValueError("Email not provided by Google")

        # Try to find an existing user or create a new one
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,  # Using email as username
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
            },
        )

        # Update profile picture if available
        if user_info.get("picture") and hasattr(user, "profile"):
            user.profile.profile_picture = cast(str, user_info.get("picture")).replace(  # type: ignore
                "s96-c", "s512-c"
            )
            user.profile.save()  # type: ignore

        return user, created


class NotVerifiedEmailError(Exception):
    """Custom exception for unverified email addresses."""
