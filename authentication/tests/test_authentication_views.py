from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from authentication.models import LoginHistory
from core.tests import AuthenticationTestCase


class AuthenticationViewsTest(AuthenticationTestCase):
    def test_registration_successful(self):
        url = reverse("authentication:auth_register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "NewPass123!",
            "password2": "NewPass123!",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registration_passwords_do_not_match(self):
        url = reverse("authentication:auth_register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "NewPass123!",
            "password2": "x!",
            "first_name": "New",
            "last_name": "User",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_get_token_pair(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        url = reverse("authentication:auth_profile")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "username": f"{self.test_user.username}",
            "email": f"{self.test_user.email}",
            "first_name": f"{self.test_user.first_name}",
            "last_name": f"{self.test_user.last_name}",
        }
        self.assertEqual(response.json(), expected)

    def test_must_be_authenticated_to_get_user_profile(self):
        url = reverse("authentication:auth_profile")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_profile(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        url = reverse("authentication:auth_profile")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "first_name": "X",
            "last_name": "Y",
            "password": self.test_user_password,
            "password2": self.test_user_password,
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            "username": f"{self.test_user.username}",
            "email": f"{self.test_user.email}",
            "first_name": f'{data["first_name"]}',
            "last_name": f'{data["last_name"]}',
        }
        self.assertEqual(response.json(), expected)

    def test_must_be_authenticated_to_patch_user_profile(self):
        data = {
            "first_name": "X",
            "last_name": "Y",
            "password": self.test_user_password,
            "password2": self.test_user_password,
        }
        url = reverse("authentication:auth_profile")
        response = self.client.patch(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_successful(self):
        token_url = reverse("authentication:token_obtain_pair")
        data = {"username": "testuser", "password": "TestPass123!"}
        token_response = self.client.post(token_url, data, format="json")
        refresh_token = token_response.data["refresh"]
        url = reverse("authentication:token_refresh")
        data = {"refresh": refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
