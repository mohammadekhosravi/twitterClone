from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .models import Tweet, Mention
from .forms import TweetForm, MentionForm
from common.decorators import ajax_required

@ajax_required
@require_POST
@login_required
def create_tweet(request):
    form = TweetForm(request.POST)
    if form.is_valid():
        author = get_user_model().objects.get(username=request.user.username)
        instance = form.save(commit=False)
        instance.author = author
        instance.save()

        return JsonResponse({
            'status': 'ok'
        })
    return JsonResponse({
        'status': 'fucked'
    })

@ajax_required
@login_required
def create_mention(request, tweet_id):
    form = MentionForm(request.POST)
    if form.is_valid():
        author = get_user_model().objects.get(username=request.user.username)
        tweet = Tweet.objects.get(id=tweet_id)
        instance = form.save(commit=False)
        instance.author = author
        instance.tweet = tweet
        instance.save()

        return JsonResponse({
            'status': 'ok'
        })
    return JsonResponse({
        'status': 'fucked'
    })



@login_required
def tweet_detail(request, pk):
    original_tweet = Tweet.objects.get(id=pk)
    context = {'form': TweetForm(),
               'mention_form': MentionForm(),
               'original_tweet': original_tweet,
               'original_tweet_author': original_tweet.author,
               'original_tweet_author_profile': original_tweet.author.profile}
    # original_tweet = original_tweet.select_related('author', 'author__profile')

    return render(request, 'tweets/detail.html', context)
