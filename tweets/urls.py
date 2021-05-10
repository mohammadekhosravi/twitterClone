from django.urls import path

from . import views

urlpatterns = [
    path('tweet/', views.create_tweet, name="create_tweet"),
    path('<int:pk>/', views.tweet_detail, name="tweet_detail"),
    path('<int:tweet_id>/mention/', views.create_mention, name="create_mention"),
]
