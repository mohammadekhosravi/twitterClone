from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
# from django.views.decorators.http import require_POST

from .models import Tweet, Mention
from .forms import TweetForm
from common.decorators import ajax_required

def create_tweet(request):
    pass
