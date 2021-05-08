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
    obj = get_object_or_404(get_user_model(),
                            username=username)
    book_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    return render(request, 'profiles/profile.html', {
        'obj': obj,
        'book_list': book_list,
    })

@login_required
def profile_following(request, username):
    obj = get_object_or_404(get_user_model(),
                            username=username)
    following = obj.following.all()

    return render(request, 'profiles/following.html', {
        'obj': obj,
        'following': following
    })

def profile_followers(request, username):
    obj = get_object_or_404(get_user_model(),
                            username=username)
    followers = obj.followers.all()

    return render(request, 'profiles/followers.html', {
        'obj': obj,
        'followers': followers,
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
            else:
                Contact.objects.filter(user_from=request.user,
                user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except get_user_model().DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
                    