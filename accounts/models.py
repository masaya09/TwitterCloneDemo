from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        error_messages={"unique": "このユーザー名はすでに使われています."},
        help_text="この項目は必須です. 150文字以下. 英数字, @/./+/-/_ だけが使えます.",
        unique=True,
        max_length=150,
        validators=[ASCIIUsernameValidator()],
        verbose_name="ユーザー名",
    )
    email = models.EmailField(
        error_messages={"unique": "このメールはすでに使われています."},
        help_text="この項目は必須です. 例:xxx@mail.com",
        unique=True,
        max_length=254,
        verbose_name="メール",
    )
    slug = models.SlugField(
        default="",
        unique=True,
        verbose_name="スラグ",
    )
    is_staff = models.BooleanField(
        verbose_name="管理者権限",
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name="アクティブ",
        default=True,
    )

    objects = UserManager()

    # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#django.contrib.auth.models.CustomUser
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)


class FriendShip(models.Model):
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_users",
        verbose_name="フォロー中",
    )
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="フォロワー",
    )

    class Meta:
        db_table = "friendship"
        verbose_name = "フォロー中・フォロワー"
        verbose_name_plural = "フォロー中・フォロワー"
        constraints = [
            models.UniqueConstraint(
                fields=["following", "follower"], name="unique_friendship"
            ),
        ]

    def __str__(self):
        return f"{self.following.username} : {self.follower.username}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
    )
    bio = models.TextField(
        blank=True,
        max_length=140,
        verbose_name="自己紹介",
    )

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
