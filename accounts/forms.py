from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)
        widgets = {
            "bio": forms.Textarea(
                attrs={"rows": 5, "cols": 30, "placeholder": "ここに入力してください"}
            ),
        }
