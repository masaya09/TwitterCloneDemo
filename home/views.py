from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView

from tweets.models import Like, Tweet

User = get_user_model()


class HomeView(LoginRequiredMixin, ListView):
    """
    GET クエリ数:7
    """

    template_name = "home/home.html"
    model = Tweet
    context_object_name = "tweets"
    paginate_by = 6
    queryset = Tweet.objects.select_related("user").prefetch_related("likes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_user = self.request.user
        context["user"] = User.objects.annotate(
            tweet_num=Count("tweets", distinct=True),
            following_num=Count("followers", distinct=True),
            follower_num=Count("following_users", distinct=True),
        ).get(username=login_user.username)
        context["liked_list"] = Like.objects.filter(user=login_user).values_list(
            "tweet", flat=True
        )
        return context
