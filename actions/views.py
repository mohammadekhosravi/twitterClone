from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Action
from tweets.models import Tweet, Mention

@login_required
def notifications(request):
    # Following notifications
    target_ct_user = ContentType.objects.get_for_model(get_user_model())
    follow_notifications = Action.objects.exclude(user=request.user).filter(target_ct=target_ct_user,
                                                               target_id=request.user.id)
    follow_notifications = follow_notifications.select_related('user', 'user__profile')\
            .prefetch_related('target')
    # tweet notifications
    target_ct_tweet = ContentType.objects.get_for_model(Tweet)
    tweet_ids = request.user.tweets.values_list('id', flat=True)
    # like tweet
    like_tweet_notifications = Action.objects.filter(target_ct=target_ct_tweet,
                                                     target_id__in=tweet_ids,
                                                     verb='like tweet')\
            .select_related('user',)\
            .prefetch_related('target', 'target__author', 'target__author__profile')
    # Mention to tweet
    mention_notifications = Action.objects.filter(target_ct=target_ct_tweet,
                                                  target_id__in=tweet_ids).exclude(verb='like tweet')\
            .select_related('user', 'user__profile')
    # like mention
    target_ct_mention = ContentType.objects.get_for_model(Mention)
    mention_ids = request.user.mentions.values_list('id', flat=True)
    like_mention_notifications = Action.objects.filter(target_ct=target_ct_mention,
                                                       target_id__in=mention_ids,
                                                       verb='like mention')\
            .select_related('user')\
            .prefetch_related('target', 'target__author', 'target__author__profile')

    return render(request, 'actions/notifications.html', {'follow_notifications': follow_notifications,
                                                          'mention_notifications': mention_notifications,
                                                          'like_tweet_notifications': like_tweet_notifications,
                                                          'like_mention_notifications': like_mention_notifications,
                                                         })
