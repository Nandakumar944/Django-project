from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Comment, Like, Notification


# -------------------------
# Auto-create or save user profile
# -------------------------
@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a Profile when a new User is created.
    Ensures the Profile is saved whenever the User is saved.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensure profile exists before saving
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()


# -------------------------
# Notify post author when a new comment is made
# -------------------------
@receiver(post_save, sender=Comment)
def notify_post_author_on_comment(sender, instance, created, **kwargs):
    """
    Creates a Notification for the post author when someone comments.
    Does not notify if the author commented on their own post.
    """
    if created and instance.post.author != instance.user:
        Notification.objects.create(
            user=instance.post.author,
            message=f"{instance.user.username} commented on your post '{instance.post.title}'",
            url=f"/post/{instance.post.id}/"
        )


# -------------------------
# Notify post author when a post is liked
# -------------------------
@receiver(post_save, sender=Like)
def notify_post_author_on_like(sender, instance, created, **kwargs):
    """
    Creates a Notification for the post author when someone likes their post.
    Does not notify if the author liked their own post.
    """
    if created and instance.post.author != instance.user:
        Notification.objects.create(
            user=instance.post.author,
            message=f"{instance.user.username} liked your post '{instance.post.title}'",
            url=f"/post/{instance.post.id}/"
        )