from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status

from blog.models import BlogPost, BlogTag
from blog.serializers import BlogPostSerializer, BlogTagSerializer


class BlogPostView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogPostSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data["author"] = request.user.pk
        return super().post(request, *args, **kwargs)


class BlogPostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogPostSerializer

    def get_object(self):
        return get_object_or_404(BlogPost, id=self.kwargs.get('id'))


class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user).order_by("-created_at")


class BlogTagView(generics.CreateAPIView):
    queryset = BlogTag.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogTagSerializer


class BlogTagListView(generics.ListAPIView):
    serializer_class = BlogTagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return BlogTag.objects.order_by("name")
