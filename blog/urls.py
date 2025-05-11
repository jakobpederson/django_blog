from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import BlogPostView

urlpatterns = [
    path('blog/', BlogPostView.as_view(), name='blog_post'),
]
