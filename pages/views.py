from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tweets.forms import TweetForm
from tweets.models import Tweet, Mention


class HomeRedirectView(RedirectView):
    permanent= True
    pattern_name = 'home'


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'


@login_required
def homepage(request):
    form = TweetForm()
    following_ids = request.user.following.values_list('id', flat=True)
    following_tweets = Tweet.objects.filter(author_id__in=following_ids)
    user_tweets = Tweet.objects.filter(author_id=request.user.id)
    all_tweets = following_tweets | user_tweets
    all_tweets = all_tweets.select_related('author', 'author__profile',).prefetch_related('mentions')

    context = {
        'form': form,
        'all_tweets': all_tweets,
    }

    return render(request, 'home.html', context)
