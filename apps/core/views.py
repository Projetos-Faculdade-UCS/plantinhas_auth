from apps.core.serializers import UserProfileSerializer

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from jwcrypto import jwk


class UserProfileView(APIView):
    """
    API view to retrieve and update user profile information.
    """

    def get(self, request):
        """
        Retrieve the user's profile information.
        """
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        """
        Update the user's profile information.
        """
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class JwksView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # Load PEM‑encoded public key
        pub_pem = settings.SIMPLE_JWT["VERIFYING_KEY"].encode("utf-8")
        # Build a JWK from it
        jwk_key = jwk.JWK.from_pem(pub_pem)
        # Export as dict to include only the public portions
        jwk_dict = jwk_key.export_public(as_dict=True)
        # Return the JWKS format
        return Response({"keys": [jwk_dict]})
