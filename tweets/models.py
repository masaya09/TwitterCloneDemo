from django.conf import settings
from django.db import models


class Tweet(models.Model):
    content = models.CharField(
        max_length=140,
        verbose_name="ツイート",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        related_name="tweets",
    )
    created_at = models.DateTimeField(
        verbose_name="作成日時",
        auto_now_add=True,
    )

    class Meta:
        db_table = "tweets"
        ordering = ["-created_at"]
        verbose_name = "ツイート"
        verbose_name_plural = "ツイート"

    def __str__(self):
        return f"{self.user.username} : {self.content}"


class Like(models.Model):
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        verbose_name="ツイート",
        related_name="likes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        related_name="likes",
    )

    class Meta:
        db_table = "like"
        verbose_name = "いいね"
        verbose_name_plural = "いいね"
        constraints = [
            models.UniqueConstraint(fields=["tweet", "user"], name="unique_like"),
        ]

    def __str__(self):
        return f"{self.user.username} : {self.tweet.content}"
