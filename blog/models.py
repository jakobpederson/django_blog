from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
