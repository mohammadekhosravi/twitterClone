from django.urls import path

from . import views

urlpatterns = [
    path('edit_profile/', views.update_profile, name="edit_profile"),
    path('follow/', views.user_follow, name="user_follow"),
    path('<username>/', views.profile, name="profile"),
    path('<username>/following/', views.profile_following, name="profile_following"),
    path('<username>/followers/', views.profile_followers, name="profile_followers"),
]