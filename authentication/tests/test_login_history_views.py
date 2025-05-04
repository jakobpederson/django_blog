from rest_framework import status
from authentication.models import LoginHistory
from django.contrib.auth.models import User
from core.tests import AuthenticationTestCase
from django.urls import reverse


class LoginHistoryViewsTest(AuthenticationTestCase):
    def test_login_history_created(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertEqual(LoginHistory.objects.count(), 1)
        login_history = LoginHistory.objects.first()
        self.assertEqual(login_history.user.id, self.test_user.id)

    def test_login_history_retrieved_successfully(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('authentication:login_history')
        response = self.client.get(url, format='json')
        self.assertEqual(LoginHistory.objects.count(), 1)
        login_history = LoginHistory.objects.first()
        expected = [
            {
                'id': login_history.id,
                'login_datetime': f'{login_history.login_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}',
                'ip_address': f'{login_history.ip_address}',
                'user_agent': f'{login_history.user_agent}'
            }
        ]
        self.assertEqual(response.json(), expected)
