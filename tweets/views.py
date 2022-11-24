from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import TweetCreateForm, TweetEditForm
from .models import Like, Tweet

User = get_user_model()


class TweetCreateView(LoginRequiredMixin, CreateView):
    """
    GET クエリ数:2
    POST クエリ数:3
    """

    form_class = TweetCreateForm
    template_name = "tweets/create.html"
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "ツイートが完了しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "ツイートが失敗しました")
        return super().form_invalid(form)


class TweetEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    GET クエリ数:4 (2 duplicates)
    POST クエリ数:5 (2 duplicates)
    """

    queryset = Tweet.objects.select_related("user")
    form_class = TweetEditForm
    template_name = "tweets/edit.html"
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        messages.success(self.request, "更新が完了しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "更新が失敗しました")
        return super().form_invalid(form)

    def test_func(self):
        # getメソッド及びpostメソッドでも
        # self:object = self.get_object()を呼び出すので、
        # test_funcでself.get_object()を呼ぶのはクエリ的にはあまり良くない
        # なので、編集ページに訪れた際、及び編集してpostした時に
        # test_funcは呼ばれるので無駄なクエリが合計で2回入る
        # https://github.com/django/django/blob/d526d1569ca4a1e62bb6a1dd779d2068766d348c/django/views/generic/edit.py#L195
        tweet = self.get_object()
        return self.request.user == tweet.user


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    GET クエリ数:4 (2 duplicates)
    POST クエリ数:7 (2 duplicates)
    """

    queryset = Tweet.objects.select_related("user")
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("home:home")
    success_message = "ツイートは削除されました"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        # updateと同様
        tweet = self.get_object()
        return self.request.user == tweet.user


class LikeView(LoginRequiredMixin, View):
    """
    POST クエリ数:7
    """

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        Like.objects.get_or_create(user=self.request.user, tweet=tweet)
        likes_count = tweet.likes.count()
        context = {
            "tweet_id": tweet.id,
            "likes_count": likes_count,
            "is_liked": True,
        }
        return JsonResponse(context)


class UnLikeView(LoginRequiredMixin, View):
    """
    POST クエリ数:7
    """

    def post(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        if like := Like.objects.filter(user=self.request.user, tweet=tweet):
            like.delete()
        likes_count = tweet.likes.count()
        context = {
            "tweet_id": tweet.id,
            "likes_count": likes_count,
            "is_liked": False,
        }
        return JsonResponse(context)
