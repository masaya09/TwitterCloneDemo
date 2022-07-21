from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from accounts.models import FriendShip
from tweets.models import Like, Tweet

User = get_user_model()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        context["tweet_list"] = Tweet.objects.select_related("user").all()
        context["tweet_num"] = (
            Tweet.objects.select_related("user").filter(user=user).count()
        )
        context["following_num"] = (
            FriendShip.objects.select_related("follower").filter(follower=user).count()
        )
        context["follower_num"] = (
            FriendShip.objects.select_related("following")
            .filter(following=user)
            .count()
        )
        context["liked_list"] = (
            Like.objects.select_related("user")
            .select_related("user")
            .filter(user=user)
            .values_list("tweet", flat=True)
        )
        return context
