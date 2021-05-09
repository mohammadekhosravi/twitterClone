from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from tweets.forms import TweetForm


class HomeRedirectView(RedirectView):
    permanent= True
    pattern_name = 'home'


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'


@login_required
def homepage(request):
    book_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    form = TweetForm()

    context = {
        'book_list': book_list,
        'form': form,
    }

    return render(request, 'home.html', context)