from django.contrib.auth.models import User
from django.db import models


class BlogTag(models.Model):
    name = models.CharField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tag: {self.name}"


class BlogCategory(models.Model):
    name = models.CharField()
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"Category: {self.name}"


class BlogPost(models.Model):
    title = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    tags = models.ManyToManyField(BlogTag, related_name="posts", blank=True)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
