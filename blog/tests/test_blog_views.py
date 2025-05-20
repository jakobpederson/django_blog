from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from authentication.models import LoginHistory
from blog.models import BlogPost
from core.factories import BlogPostFactory
from core.tests import AuthenticationTestCase


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

    def test_create_blog_post_unsuccessful_if_not_logged_in(self):
        url = reverse('blog:blog_post')
        data = {
            'title': 'first',
            'content': 'lorum ipsum',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(BlogPost.objects.count(), 0)

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
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(blog_post.id, response_json['id'])
        self.assertEqual(blog_post.title, response_json['title'])
        self.assertEqual(blog_post.content, response_json['content'])

    def test_retrieve_blog_post_unsuccessfully(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        blog_post = BlogPostFactory(author=self.test_user)
        url = reverse('blog:get_blog_post', kwargs={'id': 123})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_blog_post_successful(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        blog_post = BlogPostFactory(author=self.test_user)
        data = {
            'title': 'second',
            'content': 'second lorum ipsum',
        }
        url = reverse('blog:get_blog_post', kwargs={'id': f'{blog_post.id}'})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        blog_post.refresh_from_db()
        self.assertEqual(blog_post.id, response_json['id'])
        self.assertEqual(blog_post.title, data['title'])
        self.assertEqual(blog_post.content, data['content'])

    def test_retrieve_blog_post_list_successfully(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        url = reverse('blog:list_blog_posts')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_posts = [post["id"] for post in response.json()]
        self.assertCountEqual(blog_posts, [blog_post_1.id, blog_post_2.id])

    def test_retrieve_blog_post_list_successfully_only_gets_request_user_blog_posts(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        new_user = User.objects.create_user(
            username='newtestuser',
            email='newtest@example.com',
            password=self.test_user_password + "1"
        )
        blog_post_3 = BlogPostFactory(author=new_user)
        url = reverse('blog:list_blog_posts')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_posts = [post["id"] for post in response.json()]
        self.assertCountEqual(blog_posts, [blog_post_1.id, blog_post_2.id])

    def test_retrieve_blog_post_list_successfully_orders_by_created_most_recent(self):
        token_url = reverse('authentication:token_obtain_pair')
        token_data = {
            'username': f'{self.test_user.username}',
            'password': f'{self.test_user_password}'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        blog_post_3 = BlogPostFactory(author=self.test_user)
        url = reverse('blog:list_blog_posts')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_posts = [post["id"] for post in response.json()]
        self.assertEqual(blog_posts[0], blog_post_3.id)
        self.assertEqual(blog_posts[1], blog_post_2.id)
        self.assertEqual(blog_posts[2], blog_post_1.id)
