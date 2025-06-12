from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from authentication.models import LoginHistory
from blog.models import BlogCategory, BlogPost, BlogTag
from core.factories import BlogCategoryFactory, BlogPostFactory, BlogTagFactory
from core.tests import AuthenticationTestCase


class BlogViewsTest(AuthenticationTestCase):
    def test_create_blog_post_successful(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        url = reverse("blog:blog_post")
        data = {
            "title": "first",
            "content": "lorum ipsum",
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, data["title"])
        self.assertEqual(blog_post.content, data["content"])
        self.assertEqual(blog_post.author, self.test_user)

    def test_create_blog_post_successful_with_tags(self):
        blog_tag = BlogTagFactory()
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        url = reverse("blog:blog_post")
        data = {"title": "first", "content": "lorum ipsum", "tags": [f"{blog_tag.id}"]}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.first()
        self.assertEqual(blog_post.title, data["title"])
        self.assertEqual(blog_post.content, data["content"])
        self.assertEqual(blog_post.author, self.test_user)
        self.assertEqual(blog_post.tags.first(), blog_tag)

    def test_create_blog_post_unsuccessful_if_not_logged_in(self):
        url = reverse("blog:blog_post")
        data = {
            "title": "first",
            "content": "lorum ipsum",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_retrieve_blog_post_successful(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post = BlogPostFactory(author=self.test_user)
        url = reverse("blog:get_blog_post", kwargs={"id": f"{blog_post.id}"})
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(blog_post.id, response_json["id"])
        self.assertEqual(blog_post.title, response_json["title"])
        self.assertEqual(blog_post.content, response_json["content"])

    def test_retrieve_blog_post_unsuccessfully(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post = BlogPostFactory(author=self.test_user)
        url = reverse("blog:get_blog_post", kwargs={"id": 123})
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_blog_post_successful(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post = BlogPostFactory(author=self.test_user)
        data = {
            "title": "second",
            "content": "second lorum ipsum",
        }
        url = reverse("blog:get_blog_post", kwargs={"id": f"{blog_post.id}"})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        blog_post.refresh_from_db()
        self.assertEqual(blog_post.id, response_json["id"])
        self.assertEqual(blog_post.title, data["title"])
        self.assertEqual(blog_post.content, data["content"])

    def test_update_blog_post_with_tags_successful(self):
        blog_tag = BlogTagFactory()
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post = BlogPostFactory(author=self.test_user)
        data = {
            "title": "second",
            "content": "second lorum ipsum",
            "tags": [f"{blog_tag.id}"],
        }
        url = reverse("blog:get_blog_post", kwargs={"id": f"{blog_post.id}"})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        blog_post.refresh_from_db()
        self.assertEqual(blog_post.id, response_json["id"])
        self.assertEqual(blog_post.title, data["title"])
        self.assertEqual(blog_post.content, data["content"])
        self.assertEqual(blog_post.tags.count(), 1)
        self.assertEqual([t.id for t in blog_post.tags.all()][0], blog_tag.id)

    def test_update_blog_post_change_tags_successful(self):
        blog_tag = BlogTagFactory()
        new_blog_tag = BlogTagFactory()
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post = BlogPostFactory(author=self.test_user)
        blog_post.tags.add(blog_tag)
        data = {
            "title": "second",
            "content": "second lorum ipsum",
            "tags": [f"{new_blog_tag.id}"],
        }
        url = reverse("blog:get_blog_post", kwargs={"id": f"{blog_post.id}"})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        blog_post.refresh_from_db()
        self.assertEqual(blog_post.id, response_json["id"])
        self.assertEqual(blog_post.title, data["title"])
        self.assertEqual(blog_post.content, data["content"])
        self.assertEqual(blog_post.tags.count(), 1)
        self.assertEqual([t.id for t in blog_post.tags.all()][0], new_blog_tag.id)

    def test_retrieve_blog_post_list_successfully(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        url = reverse("blog:list_blog_posts")
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_posts = [post["id"] for post in response.json()]
        self.assertCountEqual(blog_posts, [blog_post_1.id, blog_post_2.id])

    def test_retrieve_blog_post_list_successfully_can_filter_on_author(
        self,
    ):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        new_user = User.objects.create_user(
            username="newtestuser",
            email="newtest@example.com",
            password=self.test_user_password + "1",
        )
        blog_post_3 = BlogPostFactory(author=new_user)
        url = reverse("blog:list_blog_posts")
        response = self.client.get(
            url, {"author": f"{blog_post_1.author.id}"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_posts = [post["id"] for post in response.json()]
        self.assertCountEqual(blog_posts, [blog_post_1.id, blog_post_2.id])

    def test_retrieve_blog_post_list_successfully_orders_by_created_most_recent(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        blog_post_3 = BlogPostFactory(author=self.test_user)
        url = reverse("blog:list_blog_posts")
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blog_posts = [post["id"] for post in response.json()]
        self.assertEqual(blog_posts[0], blog_post_3.id)
        self.assertEqual(blog_posts[1], blog_post_2.id)
        self.assertEqual(blog_posts[2], blog_post_1.id)

    def test_create_blog_tag_successful(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        url = reverse("blog:blog_tag")
        data = {
            "name": "first",
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogTag.objects.count(), 1)
        blog_tag = BlogTag.objects.first()
        self.assertEqual(blog_tag.name, data["name"])

    def test_retrieve_blog_tag_list_successfully(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_tag_1 = BlogTagFactory()
        blog_tag_2 = BlogTagFactory()
        url = reverse("blog:list_blog_tags")
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {"id": 1, "name": f"{blog_tag_1.name}"},
            {"id": 2, "name": f"{blog_tag_2.name}"},
        ]
        self.assertCountEqual(response.json(), expected)

    def test_retrieve_blog_category_list_successfully(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_category_1 = BlogCategoryFactory()
        blog_category_2 = BlogCategoryFactory()
        url = reverse("blog:list_blog_categories")
        response = self.client.get(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "id": 1,
                "name": f"{blog_category_1.name}",
                "slug": f"{blog_category_1.slug}",
            },
            {
                "id": 2,
                "name": f"{blog_category_2.name}",
                "slug": f"{blog_category_2.slug}",
            },
        ]
        self.assertCountEqual(response.json(), expected)

    def test_retrieve_blog_post_list_filters_by_tags(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        blog_tag_1 = BlogTagFactory()
        blog_tag_2 = BlogTagFactory()
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_1.tags.add(blog_tag_1)
        blog_post_2 = BlogPostFactory(author=self.test_user)
        blog_post_2.tags.add(blog_tag_2)
        url = reverse("blog:list_blog_posts")
        response = self.client.get(url, {"tags": f"{blog_tag_1.name}"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "title": f"{blog_post_1.title}",
                "content": f"{blog_post_1.content}",
                "author": self.test_user.id,
                "id": blog_post_1.id,
                "tags": [blog_tag_1.id],
                "category": None,
                "slug": blog_post_1.slug,
            }
        ]
        self.assertCountEqual(response.json(), expected)

    def test_retrieve_blog_post_list_filters_by_category(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        category_1 = BlogCategoryFactory()
        category_2 = BlogCategoryFactory()
        blog_post_1 = BlogPostFactory(author=self.test_user)
        blog_post_1.category = category_1
        blog_post_1.save()
        blog_post_2 = BlogPostFactory(author=self.test_user)
        blog_post_2.category = category_2
        url = reverse("blog:list_blog_posts")
        response = self.client.get(
            url, {"category": f"{category_1.name}"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "title": f"{blog_post_1.title}",
                "content": f"{blog_post_1.content}",
                "author": self.test_user.id,
                "id": blog_post_1.id,
                "tags": [],
                "category": category_1.id,
                "slug": blog_post_1.slug,
            }
        ]
        self.assertCountEqual(response.json(), expected)

    def test_create_blog_category_successful(self):
        token_url = reverse("authentication:token_obtain_pair")
        token_data = {
            "username": f"{self.test_user.username}",
            "password": f"{self.test_user_password}",
        }
        token_response = self.client.post(token_url, token_data, format="json")
        token = token_response.data["access"]
        url = reverse("blog:blog_category")
        data = {
            "name": "first",
            "slug": "lorumipsum",
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogCategory.objects.count(), 1)
        blog_category = BlogCategory.objects.first()
        self.assertEqual(blog_category.name, data["name"])
        self.assertEqual(blog_category.slug, data["slug"])
