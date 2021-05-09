from django import forms

from .models import Tweet, Mention


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ('body',)
        widgets = {'body': forms.Textarea}
