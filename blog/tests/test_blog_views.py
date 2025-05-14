from rest_framework import status
from authentication.models import LoginHistory
from django.contrib.auth.models import User
from core.tests import AuthenticationTestCase
from core.factories import BlogPostFactory
from django.urls import reverse
from blog.models import BlogPost


class BlogViewsTest(AuthenticationTestCase):
    def test_create_blog_post_successful(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        url = reverse('blog:blog_post')
        data = {
            'title': 'first',
            'content': 'lorum ipsum',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, data['title'])
        self.assertEqual(blog_post.content, data['content'])
        self.assertEqual(blog_post.author, self.test_user)

    def test_retrieve_blog_post_successful(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        blog_post = BlogPostFactory(author=self.test_user)
        url = reverse('blog:get_blog_post', kwargs={'id': f'{blog_post.id}'})
        data = {
            'id': f'{blog_post.id}',
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(blog_post.id, response_json['id'])
        self.assertEqual(blog_post.title, response_json['title'])
        self.assertEqual(blog_post.content, response_json['content'])
