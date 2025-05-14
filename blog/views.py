from rest_framework import status
from rest_framework import generics, permissions
from django.shortcuts import render

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer


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
        return self.queryset.get(id=self.kwargs.get('id'))
