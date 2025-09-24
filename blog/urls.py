from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # -------------------------
    # Home & Authentication (HTML Views)
    # -------------------------
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # -------------------------
    # Posts (HTML Views)
    # -------------------------
    path("post/create/", views.create_post, name="create_post"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/edit/", views.update_post, name="update_post"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("post/<int:pk>/like/", views.toggle_like, name="toggle_like"),
    path("post/<int:pk>/bookmark/", views.toggle_bookmark, name="toggle_bookmark"),

    # -------------------------
    # Categories & Tags
    # -------------------------
    path("category/<int:category_id>/", views.posts_by_category, name="posts_by_category"),
    path("tag/<int:tag_id>/", views.posts_by_tag, name="posts_by_tag"),

    # -------------------------
    # Profiles
    # -------------------------
    path("profile/<str:username>/", views.profile, name="profile"),

    # -------------------------
    # Comments
    # -------------------------
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),

    # -------------------------
    # Search
    # -------------------------
    path("search/", views.search_posts, name="search_posts"),

    # -------------------------
    # Notifications
    # -------------------------
    path("notifications/", views.my_notifications, name="my_notifications"),
    path("notifications/<int:pk>/read/", views.mark_notification_read, name="mark_notification_read"),

    # -------------------------
    # User Preferences
    # -------------------------
    path("toggle-theme/", views.toggle_theme, name="toggle_theme"),

    # -------------------------
    # API Authentication
    # -------------------------
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),   # DRF Token Auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # JWT Access + Refresh
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh JWT

    # -------------------------
    # Protected API Endpoint (JWT Required)
    # -------------------------
    path("api/protected/", views.my_protected_view, name="protected"),
]