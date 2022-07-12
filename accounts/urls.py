from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignUpView.as_view, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("<str:username>/", views.ProfileView.as_view(), name="profile"),
    path(
        "<str:username>/edit/",
        views.ProfileEditView.as_view(),
        name="profile_edit",
    ),
    path("<str:username>/follow/", views.follow, name="follow"),
    path("<str:username>/unfollow/", views.unfollow, name="unfollow"),
    path(
        "<str:username>/following_list/",
        views.FollowingListView.as_view(),
        name="following_list",
    ),
    path(
        "<str:username>/follower_list/",
        views.FollowerListView.as_view(),
        name="follower_list",
    ),
]