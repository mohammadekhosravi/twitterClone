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
    mentions = original_tweet.mentions.all()
    mentions = mentions.select_related('author', 'author__profile')\
            .prefetch_related('users_like')
    context = {'form': TweetForm(),
               'mention_form': MentionForm(),
               'original_tweet': original_tweet,
               'original_tweet_author': original_tweet.author,
               'original_tweet_author_profile': original_tweet.author.profile,
               'mentions': mentions,
              }
    # original_tweet = original_tweet.select_related('author', 'author__profile')

    return render(request, 'tweets/detail.html', context)

@ajax_required
@login_required
def like_unlike(request):
    pk = request.POST.get('pk')
    like_type = request.POST.get('type')
    # determine that like is for mention or tweet
    if like_type == 'tweet':
        tweet = Tweet.objects.get(pk=pk)
    else:
        tweet  = Mention.objects.get(pk=pk)

    if request.user in tweet.users_like.all():
        tweet.users_like.remove(request.user)
    else:
        tweet.users_like.add(request.user)
    return JsonResponse({'like_count': tweet.like_count})
