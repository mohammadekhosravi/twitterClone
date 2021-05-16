from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector,\
        SearchQuery, SearchRank

from .models import Tweet, Mention
from .forms import TweetForm, MentionForm
from common.decorators import ajax_required
from actions.utils import create_action

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

# @ajax_required
# @require_POST
@login_required
def delete_tweet(request):
    pk = request.POST.get('pk')
    # delete tweet
    tweet = get_object_or_404(Tweet, pk=pk)
    tweet.delete()
    # go to profile page
    obj = get_object_or_404(get_user_model(), username=request.user.username)
    obj_profile = obj.profile
    all_tweets = obj.tweets.all().select_related('author', 'author__profile')\
            .prefetch_related('mentions', 'users_like')
    form = TweetForm()
    context = {
        'obj': obj,
        'obj_profile': obj_profile,
        'all_tweets': all_tweets,
        'form': form,
        'tweet_and_mention_count': all_tweets.count() + obj.mentions.all().count()
    }

    return render(request, 'profiles/profile.html', context)


@ajax_required
@login_required
def create_mention(request, tweet_id):
    form = MentionForm(request.POST)
    if form.is_valid():
        author = get_user_model().objects.get(username=request.user.username)
        tweet = Tweet.objects.get(id=tweet_id)
        user = tweet.author
        instance = form.save(commit=False)
        instance.author = author
        instance.tweet = tweet
        instance.save()

        create_action(request.user, instance.mention, tweet)
        return JsonResponse({
            'status': 'ok'
        })
    return JsonResponse({
        'status': 'fucked'
    })



@login_required
def tweet_detail(request, pk):
    original_tweet = get_object_or_404(Tweet, id=pk)
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
        action_verb = 'like tweet'
    else:
        tweet  = Mention.objects.get(pk=pk)
        action_verb = 'like mention'

    if request.user in tweet.users_like.all():
        tweet.users_like.remove(request.user)
    else:
        tweet.users_like.add(request.user)
        create_action(request.user, action_verb, tweet)
    return JsonResponse({'like_count': tweet.like_count})

@login_required
def search(request):
    form = TweetForm()
    query = request.GET.get('search')

    # Building search results include Stemming and ranking results
    search_vector = SearchVector('body', weight='A')
    search_query = SearchQuery(query)
    results = Tweet.objects.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.2).order_by('-rank')

    # Fetch related models
    results = results.select_related('author', 'author__profile',)\
            .prefetch_related('mentions', 'users_like')

    context = {'query': query,
               'results': results,
               'form': form,
              }
    return render(request, 'tweets/search.html', context)
