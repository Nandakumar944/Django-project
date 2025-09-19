from django.contrib import admin
from .models import (
    Post, Category, Tag, Profile,
    Comment, Like, Bookmark, Notification
)

# -------------------------
# Category Admin
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}  # auto-generate slug


# -------------------------
# Tag Admin
# -------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}  # auto-generate slug


# -------------------------
# Post Admin
# -------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'status', 'created_at', 'updated_at', 'publish_date')
    list_filter = ('status', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)


# -------------------------
# Profile Admin
# -------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme_preference', 'website', 'twitter')
    search_fields = ('user__username', 'bio', 'website', 'twitter')


# -------------------------
# Comment Admin
# -------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'parent', 'created_at')
    search_fields = ('post__title', 'user__username', 'text')
    list_filter = ('created_at',)


# -------------------------
# Like Admin
# -------------------------
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)


# -------------------------
# Bookmark Admin
# -------------------------
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)


# -------------------------
# Notification Admin
# -------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read', 'created_at')