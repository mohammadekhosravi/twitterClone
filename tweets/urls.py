from django.urls import path

from . import views

urlpatterns = [
    path('tweet/', views.create_tweet, name="create_tweet"),
]
