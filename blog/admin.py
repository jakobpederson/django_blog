from django.contrib import admin

from blog import models


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "author")
    list_filter = ("title", "author")
    search_fields = ("title", "author")


@admin.register(models.BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
