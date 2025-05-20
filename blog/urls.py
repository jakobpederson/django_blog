from django.urls import path

from .views import BlogPostListView, BlogPostRetrieveUpdateView, BlogPostView

urlpatterns = [
    path('blog/', BlogPostView.as_view(), name='blog_post'),
    path('blog/<int:id>', BlogPostRetrieveUpdateView.as_view(), name='get_blog_post'),
    path('blog/posts/', BlogPostListView.as_view(), name='list_blog_posts'),
]
