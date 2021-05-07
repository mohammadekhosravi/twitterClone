from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'avatar',)
        widgets = {'bio': forms.Textarea}
