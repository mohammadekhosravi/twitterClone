from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
# For AJAX
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact

from .forms import UserForm, ProfileForm
from actions.utils import create_action
from tweets.forms import TweetForm
from tweets.models import Tweet

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', request.user)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request, username):
    
    obj = get_object_or_404(get_user_model(), username=username)
    obj_profile = obj.profile
    all_tweets = obj.tweets.all().select_related('author', 'author__profile')\
            .prefetch_related('mentions')
    form = TweetForm()
    context = {
        'obj': obj,
        'obj_profile': obj_profile,
        'all_tweets': all_tweets,
        'form': form,
    }

    return render(request, 'profiles/profile.html', context)

@login_required
def profile_following(request, username):
    obj = get_object_or_404(get_user_model(),
                            username=username)
    following = obj.following.all().select_related('profile')
    request_user_following = request.user.following.all()

    return render(request, 'profiles/following.html', {
        'obj': obj,
        'following': following,
        'request_user_following': request_user_following,
    })

def profile_followers(request, username):
    obj = get_object_or_404(get_user_model(),
                            username=username)
    followers = obj.followers.all().select_related('profile')
    request_user_following = request.user.following.all()

    return render(request, 'profiles/followers.html', {
        'obj': obj,
        'followers': followers,
        'request_user_following': request_user_following,
    })

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = get_user_model().objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                ) 
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                user_to=user).delete()
            followers_count = user.followers.all().count()
            following_count = user.following.all().count()
            return JsonResponse({'status': 'ok',
            'following_count': str(following_count),
            'followers_count': str(followers_count),
            })
        except get_user_model().DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
