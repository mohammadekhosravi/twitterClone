from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeRedirectView.as_view(), name='home_redirect'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
]
