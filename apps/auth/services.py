# Your services go here

from typing import Any
from typing import Dict
from typing import Optional

from django.conf import settings

from google.auth.transport import requests
from google.oauth2 import id_token


class GoogleOAuthService:
    # Google OAuth Client IDs from settings
    WEB_CLIENT_ID = settings.GOOGLE_OAUTH.get("WEB_CLIENT_ID")
    # Add more client IDs if needed
    ALLOWED_CLIENT_IDS = [WEB_CLIENT_ID]
    # Optional: specify allowed domain
    ALLOWED_DOMAIN = settings.GOOGLE_OAUTH.get("ALLOWED_DOMAIN")

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
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), cls.WEB_CLIENT_ID
            )

            # If you have multiple client IDs, use this approach instead:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in cls.ALLOWED_CLIENT_IDS:
            #     raise ValueError('Could not verify audience.')

            # Check domain if specified
            if cls.ALLOWED_DOMAIN and idinfo.get("hd") != cls.ALLOWED_DOMAIN:
                raise ValueError("Wrong domain name.")

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
