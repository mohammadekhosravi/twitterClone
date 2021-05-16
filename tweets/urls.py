from django.urls import path

from . import views

urlpatterns = [
    path('tweet/', views.create_tweet, name="create_tweet"),
    path('like-unlike/', views.like_unlike, name="like-unlike"),
    path('<int:pk>/', views.tweet_detail, name="tweet_detail"),
    path('<int:tweet_id>/mention/', views.create_mention, name="create_mention"),
    path('search/', views.search, name="search"),
]
