from django.contrib import admin

from .models import Tweet, Mention

@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ('author', 'tweet', 'get_body', 'like_count', 'created')
    list_filter = ('created',)
    search_fields = ('body', 'tweet')

    def get_body(self, instance):
        return instance.body[:20] + ' ...'
    get_body.short_description = 'Body'


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_body', 'like_count', 'created')
    list_filter = ('created',)
    search_fields = ('body',)

    def get_body(self, instance):
        return instance.body[:20] + ' ...'
    get_body.short_description = 'Body'
