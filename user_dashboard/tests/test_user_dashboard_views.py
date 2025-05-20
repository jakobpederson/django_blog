from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from authentication.models import LoginHistory
from core.tests import AuthenticationTestCase
from user_dashboard.models import UserProfile


class UserDashboardViewsTest(AuthenticationTestCase):
    def test_get_user_dashboard_successfully(self):
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
            'first_name': f'{self.test_user.first_name}',
            'last_name': f'{self.test_user.last_name}',
            'profile': {
                'id': test_user_profile.id,
                'bio': f'{test_user_profile.bio}',
                'location': f'{test_user_profile.location}',
                'date_of_birth': f'{test_user_profile.date_of_birth}'
            }
        }
        self.assertEqual(response.json(), expected)

    def test_update_user_dashboard(self):
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
        data = {
            'profile': {
                'bio': 'newbio',
                'location': 'newlocation',
                'date_of_birth': '2024-01-01',
            },
            'username': 'newusername',
            'first_name': 'newfirst',
            'last_name': 'newlast',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {
            'id': self.test_user.id,
            'username': f'{data["username"]}',
            'first_name': f'{data["first_name"]}',
            'last_name': f'{data["last_name"]}',
            'profile': {
                'id': test_user_profile.id,
                'bio': f'{data["profile"]["bio"]}',
                'location': f'{data["profile"]["location"]}',
                'date_of_birth': f'{data["profile"]["date_of_birth"]}'
            }
        }
        self.assertEqual(response.json(), expected)
