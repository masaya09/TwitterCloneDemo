from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, verbose_name="Eメール")

    class Meta:
        db_table = "users"
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def __str__(self):
        return self.username


class FriendShip(models.Model):
    following = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE, verbose_name="フォロー"
    )
    follower = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE, verbose_name="フォロワー"
    )

    class Meta:
        db_table = "friendship"
        verbose_name = "フォロー・フォロワー"
        verbose_name_plural = "フォロー・フォロワー"
        constraints = [
            models.UniqueConstraint(
                fields=["following", "follower"], name="unique_friendship"
            ),
        ]

    def __str__(self):
        return f"{self.following.username} : {self.follower.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    bio = models.TextField(blank=True, null=True, max_length=140, verbose_name="自己紹介")

    class Meta:
        db_table = "profile"
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィール"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.save()
