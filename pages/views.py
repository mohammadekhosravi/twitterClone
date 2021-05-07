from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeRedirectView(RedirectView):
    permanent= True
    pattern_name = 'home'


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomePageView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        return context


class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
