from django.urls import path

from .views import (
    BlogCategoryListView,
    BlogCategoryView,
    BlogPostListView,
    BlogPostRetrieveUpdateView,
    BlogPostView,
    BlogTagListView,
    BlogTagView,
)

urlpatterns = [
    path("blog/", BlogPostView.as_view(), name="blog_post"),
    path("blog/<int:id>", BlogPostRetrieveUpdateView.as_view(), name="get_blog_post"),
    path("blog/posts/", BlogPostListView.as_view(), name="list_blog_posts"),
    path("blog/tags/", BlogTagView.as_view(), name="blog_tag"),
    path("blog/tags/list/", BlogTagListView.as_view(), name="list_blog_tags"),
    path(
        "blog/categories/list/",
        BlogCategoryListView.as_view(),
        name="list_blog_categories",
    ),
    path(
        "blog/categories",
        BlogCategoryView.as_view(),
        name="blog_category",
    ),
]
