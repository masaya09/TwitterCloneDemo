from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from accounts.models import FriendShip
from tweets.models import Like, Tweet

User = get_user_model()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        ctx["tweet_list"] = Tweet.objects.select_related("user").all()
        ctx["following_num"] = (
            FriendShip.objects.select_related("following")
            .filter(following=user)
            .count()
        )
        ctx["follower_num"] = (
            FriendShip.objects.select_related("follower").filter(follower=user).count()
        )
        ctx["liked_list"] = (
            Like.objects.select_related("user")
            .select_related("user")
            .filter(user=user)
            .values_list("tweet", flat=True)
        )
        return ctx
