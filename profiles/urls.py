from django.urls import path

from . import views

urlpatterns = [
    path('edit_profile/', views.update_profile, name="edit_profile"),
    path('<username>/', views.profile, name="profile"),
]
