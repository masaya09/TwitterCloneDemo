from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import TweetCreateForm, TweetEditForm
from .models import Like, Tweet

User = get_user_model()


class TweetCreateView(LoginRequiredMixin, CreateView):
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
    model = Tweet
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
        tweet = self.get_object()
        return self.request.user == tweet.user


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("home:home")
    success_message = "ツイートは削除されました"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.user


@login_required
@require_POST
def like(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    Like.objects.get_or_create(user=request.user, tweet=tweet)
    is_liked = True
    likes_count = tweet.like_set.count()
    context = {
        "tweet_id": tweet.id,
        "likes_count": likes_count,
        "is_liked": is_liked,
    }
    return JsonResponse(context)


@login_required
@require_POST
def unlike(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if like := Like.objects.filter(user=request.user, tweet=tweet):
        like.delete()
    is_liked = False
    likes_count = tweet.like_set.count()
    context = {
        "tweet_id": tweet.id,
        "likes_count": likes_count,
        "is_liked": is_liked,
    }
    return JsonResponse(context)
