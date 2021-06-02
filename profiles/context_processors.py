"""
Add 'suggestion' to context of all templates for follow suggestion section of site.
"""
from django.contrib.auth import get_user_model
from django.db.models import Count

def follow_suggestion(request):
    if request.user.is_authenticated:
        following_ids = request.user.following.values_list('id', flat=True)
        suggestion = get_user_model().objects.all().exclude(id__in=following_ids).exclude(username=request.user.username)
        suggestion = suggestion.annotate(followers_count=Count('followers')).order_by('-followers_count')[:3]

        return {'suggestion': suggestion}
    return {'suggestion': None}
