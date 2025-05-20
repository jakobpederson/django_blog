from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import LoginHistory


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user_password = 'TestPass123!'
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=self.test_user_password
        )

        # Setup the API client
        self.client = APIClient()
