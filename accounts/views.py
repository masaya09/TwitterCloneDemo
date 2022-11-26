from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView

from tweets.models import Like

from .forms import ProfileEditForm, SignUpForm
from .models import FriendShip

User = get_user_model()


class SignUpView(CreateView):
    """
    GET クエリ数:0
    POST クエリ数: 11 session状況によって12
    """

    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        # authenticateでEmailAuthenticationBackendを呼び出している
        # EmailAuthenticationBackendを用いなくても、
        # USERNAME_FIELDにemailを設定していれば実際のところ必要ないが
        # あえて記述し、email=emailと書けるようにしている
        user = authenticate(self.request, email=email, password=password)
        login(self.request, user)
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    """
    GET クエリ数:7
    """

    template_name = "accounts/profile.html"

    def get_queryset(self):
        return (
            User.objects.filter(slug=self.kwargs["slug"])
            .select_related("profile")
            .annotate(
                tweet_num=Count("tweets", distinct=True),
                following_num=Count("followers", distinct=True),
                follower_num=Count("following_users", distinct=True),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tweets"] = self.object.tweets.prefetch_related("likes").all()
        context["liked_list"] = Like.objects.filter(user=self.request.user).values_list(
            "tweet", flat=True
        )
        if self.request.user != self.object:
            context["is_following"] = FriendShip.objects.filter(
                following=self.object, follower=self.request.user
            ).exists()
        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    GET クエリ数:3
    POST クエリ数:4
    """

    queryset = User.objects.select_related("profile")
    form_class = ProfileEditForm
    template_name = "accounts/profile_edit.html"

    def get_object(self):
        target_user = get_object_or_404(self.queryset, slug=self.kwargs["slug"])
        return target_user.profile

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"slug": self.request.user.slug})

    def test_func(self):
        return self.request.user.slug == self.kwargs["slug"]


class FollowView(LoginRequiredMixin, View):
    """
    POST クエリ数:5
    """

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        # self.kwargs["slug"]だとTypeError
        # got an unexpected keyword argument 'slug'
        following = get_object_or_404(User, slug=kwargs["slug"])
        if follower == following:
            messages.warning(self.request, "自分をフォローすることはできません")
        elif FriendShip.objects.filter(follower=follower, following=following).exists():
            messages.warning(self.request, f"あなたはすでに{ following.username }をフォローしています")
        else:
            FriendShip(follower=follower, following=following).save()
        return redirect("home:home")


class UnFollowView(LoginRequiredMixin, View):
    """
    POST クエリ数:6
    """

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        following = get_object_or_404(User, slug=kwargs["slug"])
        if FriendShip.objects.filter(follower=follower, following=following).exists():
            FriendShip.objects.filter(follower=follower, following=following).delete()
        else:
            messages.warning(self.request, "無効な操作です")
        return redirect("home:home")


class FollowingListView(LoginRequiredMixin, DetailView):
    """
    GET クエリ数:5 (2 similar)
    """

    model = User
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following_users = FriendShip.objects.filter(follower=self.object).values_list(
            "following"
        )
        context["following_list"] = User.objects.filter(id__in=following_users)
        following_users_by_login_user = (
            FriendShip.objects.select_related("follower")
            .filter(follower=self.request.user)
            .values_list("following")
        )
        context["following_by_login_user"] = User.objects.filter(
            id__in=following_users_by_login_user
        )
        return context


class FollowerListView(LoginRequiredMixin, DetailView):
    """
    GET クエリ数:5
    """

    model = User
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followers = FriendShip.objects.filter(following=self.object).values_list(
            "follower"
        )
        context["follower_list"] = User.objects.filter(id__in=followers)
        following_users_by_login_user = FriendShip.objects.filter(
            follower=self.request.user
        ).values_list("following")
        context["following_by_login_user"] = User.objects.filter(
            id__in=following_users_by_login_user
        )
        return context
