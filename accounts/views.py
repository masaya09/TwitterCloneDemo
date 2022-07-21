from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from tweets.models import Tweet

from .forms import ProfileEditForm, SignUpForm
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

    def get_object(self):
        target_user = get_object_or_404(User, username=self.kwargs["username"])
        return target_user.profile

    def get_queryset(self):
        return Tweet.objects.select_related("user").filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["following_num"] = (
            FriendShip.objects.select_related("follower").filter(follower=user).count()
        )
        context["follower_num"] = (
            FriendShip.objects.select_related("following")
            .filter(following=user)
            .count()
        )
        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"

    def get_object(self):
        target_user = get_object_or_404(User, username=self.kwargs["username"])
        return target_user.profile

    def get_success_url(self):
        return reverse(
            "accounts:profile", kwargs={"username": self.request.user.username}
        )

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


@login_required
def follow(request, **kwargs):
    follower = request.user
    following = get_object_or_404(User, username=kwargs["username"])
    if follower == following:
        messages.warning(request, "自分をフォローすることはできません")
    elif FriendShip.objects.filter(follower=follower, following=following).exists():
        messages.warning(request, f"あなたはすでに{ following.username }をフォローしています")
    else:
        FriendShip(follower=follower, following=following).save()
    return redirect("home:home")


@login_required
def unfollow(request, **kwargs):
    follower = request.user
    following = get_object_or_404(User, username=kwargs["username"])
    if FriendShip.objects.filter(follower=follower, following=following).exists():
        FriendShip.objects.filter(follower=follower, following=following).delete()
    else:
        messages.warning(request, "無効な操作です")
    return redirect("home:home")


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followings = (
            FriendShip.objects.select_related("following", "follower")
            .filter(follower=user)
            .values_list("following")
        )
        context["following_list"] = User.objects.filter(id__in=followings)
        print(followings)
        return context


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followings = (
            FriendShip.objects.select_related("following", "follower")
            .filter(follower=user)
            .values_list("following")
        )
        context["following_list"] = User.objects.filter(id__in=followings)
        followers = (
            FriendShip.objects.select_related("following", "follower")
            .filter(following=user)
            .values_list("follower")
        )
        context["follower_list"] = User.objects.filter(id__in=followers)
        print(followings)
        print(followers)
        print(context["following_list"])
        print(context["follower_list"])
        return context
