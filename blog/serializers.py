from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'author', 'id')

    def create(self, validated_data):
        blog_post = BlogPost.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            author=validated_data['author'],
        )
        return blog_post
