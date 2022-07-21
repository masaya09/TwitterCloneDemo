from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tweet(models.Model):
    content = models.TextField(verbose_name="ツイート", max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
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
        Tweet, on_delete=models.CASCADE, verbose_name="ツイート", related_name="tweet"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="ユーザー", related_name="user"
    )

    class Meta:
        db_table = "like"
        verbose_name = "いいね"
        verbose_name_plural = "いいね"

    def __str__(self):
        return f"{self.user.username} : {self.tweet.content}"
