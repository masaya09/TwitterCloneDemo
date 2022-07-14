from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from tweets.models import Tweet

from .forms import SignUpForm
from .models import FriendShip, Profile

User = get_user_model()


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


class ProfileView(LoginRequiredMixin, ListView):
    model = Tweet
    context_object_name = "tweets"
    template_name = "accounts/profile.html"
    fields = ("user", "bio")

    def get_queryset(self):
        return Tweet.objects.select_related("user").filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["following_num"] = (
            FriendShip.objects.select_related("following")
            .filter(following=user)
            .count()
        )
        ctx["follower_num"] = (
            FriendShip.objects.select_related("follower").filter(follower=user).count()
        )
        return ctx


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile

    def get_success_url(self):
        return reverse(
            "accounts:profile", kwargs={"username": self.request.user.username}
        )

    def test_func(self):
        return self.request.user.username == self.kwargs["username"]


@login_required
def follow(self, request, *args, **kwargs):
    follower = get_object_or_404(User, username=request.user.username)
    following = get_object_or_404(User, username=self.kwargs["username"])
    if follower == following:
        messages.warning(request, "自分をフォローすることはできません")
    elif FriendShip.objects.filter(follower=follower, following=following).exists():
        messages.warning(request, f"あなたはすでに{ following.username }をフォローしています")
    else:
        FriendShip(follower=follower, following=following).save()
    return redirect("home:home")


@login_required
def unfollow(self, request, *args, **kwargs):
    follower = get_object_or_404(User, username=request.user.username)
    following = get_object_or_404(User, username=self.kwargs["username"])
    if FriendShip.objects.filter(follower=follower, following=following).exists():
        FriendShip.objects.filter(follower=follower, following=following).delete()
    else:
        messages.warning(request, "無効な操作です")
    return redirect("home:home")


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["following_list"] = FriendShip.objects.select_related(
            "following", "follower"
        ).filter(following=user)
        return ctx


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["following_list"] = FriendShip.objects.select_related(
            "following", "follower"
        ).filter(following=user)
        ctx["follower_list"] = FriendShip.objects.select_related(
            "following", "follower"
        ).filter(follower=user)
        return ctx
