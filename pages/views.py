from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeRedirectView(RedirectView):
    permanent= True
    pattern_name = 'home'


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
