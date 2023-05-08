from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseRedirect
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
    GET クエリ数:3
    POST クエリ数:4
    """

    queryset = Tweet.objects.select_related("user")
    form_class = TweetEditForm
    template_name = "tweets/edit.html"
    success_url = reverse_lazy("home:home")

    def get(self, request, *args, **kwargs):  # self.get_object()を呼び出すのを防ぐためにオーバーライド
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):  # self.get_object()を呼び出すのを防ぐためにオーバーライド
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "更新が完了しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "更新が失敗しました")
        return super().form_invalid(form)

    def test_func(self):
        self.object = self.get_object()
        return self.request.user == self.object.user


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    GET クエリ数:3
    POST クエリ数:6
    """

    queryset = Tweet.objects.select_related("user")
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("home:home")
    success_message = "ツイートは削除されました"

    def get(self, request, *args, **kwargs):  # self.get_object()を呼び出すのを防ぐためにオーバーライド
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):  # self.get_object()を呼び出すのを防ぐためにオーバーライド
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):  # self.get_object()を呼び出すのを防ぐためにオーバーライド
        messages.success(self.request, self.success_message)
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def test_func(self):
        self.object = self.get_object()
        return self.request.user == self.object.user


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
