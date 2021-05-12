from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeRedirectView.as_view(), name='home_redirect'),
    path('home/', views.homepage, name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
]
