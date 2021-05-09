from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Action

@login_required
def notifications(request):
    # Display 'is following' actions
    target_ct_user = ContentType.objects.get_for_model(get_user_model())
    follow_notifications = Action.objects.exclude(user=request.user).filter(target_ct=target_ct_user,
                                                               target_id=request.user.id)

    return render(request, 'actions/notifications.html', {'follow_notifications': follow_notifications})
