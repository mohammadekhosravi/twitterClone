from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .models import Tweet, Mention
from .forms import TweetForm
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