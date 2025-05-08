from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class AdminLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("admin-login")

        # Create a regular user
        self.regular_user = User.objects.create_user(
            username="regularuser",
            email="regularuser@example.com",
            password="regularpass123",
        )

        # Create an admin user
        self.admin_user = User.objects.create_user(
            username="adminuser", email="adminuser@example.com", password="adminpass123"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()

    def test_login_success_admin(self):
        """Test that admins can login successfully and get tokens"""
        payload = {"username": "adminuser", "password": "adminpass123"}

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("exp", response.data)

    def test_login_fail_regular_user(self):
        """Test that regular users cannot use the admin login endpoint"""
        payload = {"username": "regularuser", "password": "regularpass123"}

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User is not authorized", str(response.data))

    def test_login_fail_invalid_credentials(self):
        """Test that login fails with invalid credentials"""
        payload = {"username": "adminuser", "password": "wrongpassword"}

        response = self.client.post(self.login_url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Unable to log in", str(response.data))
