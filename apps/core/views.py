from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.serializers import UserProfileSerializer


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
