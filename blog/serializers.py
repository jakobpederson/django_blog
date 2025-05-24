from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from blog.models import BlogPost, BlogTag


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'author', 'id', 'tags')

    def create(self, validated_data):
        tags = validated_data.get("tags")
        blog_post = BlogPost.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            author=validated_data['author'],
        )
        if tags:
            blog_post.tags.add(*tags)
        return blog_post


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ('name',)
