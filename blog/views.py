from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, PostForm, CommentForm
from .models import Post, Category, Tag, Comment, Bookmark, Like, Notification, Profile
from django.http import JsonResponse
import json

# ---- DRF imports for JWT ----
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# -------------------------
# Theme toggle
# -------------------------
@login_required
def toggle_theme(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.theme_preference = "dark" if profile.theme_preference == "light" else "light"
    profile.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


# -------------------------
# Notifications
# -------------------------
@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "blog/notifications.html", {"notifications": notifications})


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.url or "my_notifications")


# -------------------------
# Bookmarks
# -------------------------
@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related("post")
    return render(request, "blog/my_bookmarks.html", {"bookmarks": bookmarks})


@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if not created:
        bookmark.delete()
        messages.info(request, "Removed from bookmarks.")
    else:
        messages.success(request, "Post saved to bookmarks.")
    return redirect('post_detail', pk=pk)


# -------------------------
# Likes
# -------------------------
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        messages.info(request, "You unliked this post.")
    else:
        messages.success(request, "You liked this post.")
    return redirect('post_detail', pk=pk)


# -------------------------
# Home and filters
# -------------------------
def home(request):
    posts = Post.objects.filter(approved=True).order_by('-created_at')
    return render(request, "blog/home.html", {"posts": posts})


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, approved=True)
    return render(request, "blog/home.html", {"posts": posts, "filter": f"Category: {category.name}"})


def posts_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag, approved=True)
    return render(request, "blog/home.html", {"posts": posts, "filter": f"Tag: {tag.name}"})


def search_posts(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        approved=True
    ) if query else []
    return render(request, "blog/home.html", {"posts": posts, "filter": f"Search: {query}" if query else None})


# -------------------------
# Authentication
# -------------------------
def register(request):
    if request.method == "POST":
        print(request.POST)
        if request.content_type == "application/json":
            data = json.loads(request.body.decode("utf-8"))
            form = UserRegisterForm(data)
        else:
            form = UserRegisterForm(request.POST)
        print(form.errors, form.cleaned_data)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            return JsonResponse({
                "status": "success",
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            })
        else:
            if request.headers.get("Accept") == "application/json":
                return JsonResponse({
                    "status": "error",
                    "errors": form.errors
                }, status=400)
    else:
        form = UserRegisterForm()

    return render(request, "blog/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)   # session login
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


# -------------------------
# Profile
# -------------------------
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile_info = getattr(user_profile, 'profile', None)

    posts = Post.objects.filter(author=user_profile, approved=True)
    liked_posts = Post.objects.filter(likes__user=user_profile, approved=True).distinct()
    bookmarked_posts = Post.objects.filter(bookmarked_by__user=user_profile, approved=True).distinct()

    return render(request, 'blog/profile.html', {
        'user_profile': user_profile,
        'profile_info': profile_info,
        'posts': posts,
        'liked_posts': liked_posts,
        'bookmarked_posts': bookmarked_posts,
    })


# -------------------------
# Post detail & comments
# -------------------------
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, approved=True)
    comments = post.comments.all().values("id", "user__username", "text", "created_at")

    if request.method == "GET":
        return JsonResponse({
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
            },
            "comments": list(comments),
        }, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_superuser or request.user == comment.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)


# -------------------------
# Post CRUD
# -------------------------
@login_required
@csrf_exempt  # only for API testing
def create_post(request):
    if request.method == "POST":
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            form = PostForm(data)
        else:
            form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Post created successfully",
                    "post": {
                        "id": post.pk,
                        "title": post.title,
                        "content": post.content,
                        "author": post.author.username,
                    },
                },
                status=201,
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post_detail", pk=post.pk)
    return render(request, "blog/post_form.html", {"form": form, "title": "Edit Post"})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "blog/post_confirm_delete.html", {"post": post})


# -------------------------
# JWT Protected Test Endpoint
# -------------------------
"""@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    return Response({"message": f"Hello {request.user.username}, you are authenticated via JWT!"})"""

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    print("Authorization header:", request.headers.get("Authorization"))
    return Response({"message": f"Hello {request.user.username}, you are authenticated!"})