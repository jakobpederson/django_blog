from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import BlogPostView, BlogPostRetrieveUpdateView

urlpatterns = [
    path('blog/', BlogPostView.as_view(), name='blog_post'),
    path('blog/<id>', BlogPostRetrieveUpdateView.as_view(), name='get_blog_post'),
]
