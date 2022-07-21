from django import forms

from .models import Tweet


class TweetBaseForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 5, "cols": 30, "placeholder": "ここに入力してください"}
            ),
        }


class TweetCreateForm(TweetBaseForm):
    pass


class TweetEditForm(TweetBaseForm):
    class Meta(TweetBaseForm.Meta):
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5, "cols": 30}),
        }
