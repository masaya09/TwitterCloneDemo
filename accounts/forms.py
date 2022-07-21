from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        help_texts = {"email": _("この項目は必須です。 例：xxx@mail.com")}


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)
        widgets = {
            "bio": forms.Textarea(
                attrs={"rows": 5, "cols": 30, "placeholder": "ここに入力してください"}
            ),
        }
