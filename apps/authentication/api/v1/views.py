from django.conf import settings
from django.http import JsonResponse
from django.views import View

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jwcrypto import jwk

from .serializers import GoogleAuthSerializer


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # Extract token from Authorization header
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        print(auth_header)

        # Typically format is "Bearer <token>"
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            return Response(
                {"error": "Authorization header must start with 'Bearer'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Pass token to serializer
        serializer = GoogleAuthSerializer(data={"token": token})
        if serializer.is_valid():
            auth_data = serializer.save()
            return Response(auth_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JwksView(View):
    def get(self, request):
        # Load PEM‑encoded public key
        pub_pem = settings.SIMPLE_JWT["VERIFYING_KEY"].encode("utf-8")
        # Build a JWK from it
        jwk_key = jwk.JWK.from_pem(pub_pem)
        # Export as dict to include only the public portions
        jwk_dict = jwk_key.export_public(as_dict=True)
        # Return the JWKS format
        return JsonResponse({"keys": [jwk_dict]})
