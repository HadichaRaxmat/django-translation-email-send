from django.contrib import admin
from .models import Post, Contact


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title", "text")
    list_filter = ("title",)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
