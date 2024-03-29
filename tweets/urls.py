from django.urls import path

from . import views

app_name = "tweets"

urlpatterns = [
    path("create", views.TweetCreateView.as_view(), name="create"),
    path("<int:pk>/edit", views.TweetEditView.as_view(), name="edit"),
    path("<int:pk>/delete", views.TweetDeleteView.as_view(), name="delete"),
    path("<int:pk>/like", views.LikeView.as_view(), name="like"),
    path("<int:pk>/unlike", views.UnLikeView.as_view(), name="unlike"),
]
