from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path(
        "<slug:slug>/edit",
        views.ProfileEditView.as_view(),
        name="profile_edit",
    ),
    path("<slug:slug>/follow/", views.FollowView.as_view(), name="follow"),
    path("<slug:slug>/unfollow/", views.UnFollowView.as_view(), name="unfollow"),
    path(
        "<slug:slug>/following_list/",
        views.FollowingListView.as_view(),
        name="following_list",
    ),
    path(
        "<slug:slug>/follower_list/",
        views.FollowerListView.as_view(),
        name="follower_list",
    ),
]
