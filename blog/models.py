from django.contrib.auth.models import User
from django.db import models


class BlogTag(models.Model):
    name = models.CharField()
    created_at = models.DateTimeField(auto_now=True)


class BlogPost(models.Model):
    title = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(BlogTag, related_name="posts", blank=True, null=True)
