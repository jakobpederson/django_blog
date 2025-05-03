from rest_framework import status
from authentication.models import LoginHistory
from django.contrib.auth.models import User
from user_dashboard.models import UserProfile
from core.tests import AuthenticationTestCase
from django.urls import reverse


class UserDashboardViewsTest(AuthenticationTestCase):
    def test_get_user_dashboard(self):
        test_user_profile = UserProfile.objects.create(user=self.test_user, bio="bio123", location="location123", date_of_birth="2024-05-24")
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        url = reverse('user_dashboard:dashboard')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'id': self.test_user.id,
            'username': f'{self.test_user.username}',
            'profile': {
                'id': test_user_profile.id,
                'bio': f'{test_user_profile.bio}',
                'location': f'{test_user_profile.location}',
                'date_of_birth': f'{test_user_profile.date_of_birth}'
            }
        }
        self.assertEqual(response.json(), expected)
