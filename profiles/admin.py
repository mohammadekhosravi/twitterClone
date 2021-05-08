from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile, Contact

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class ContactInline(admin.StackedInline):
    model = Contact
    con_delete = False
    verbose_name_plural = 'Contact'
    fk_name = 'user_from'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, ContactInline,)
    list_display = ('username', 'get_following', 'get_followers', 'get_bio', 'get_name', 'email', 'is_staff')
    list_select_related = ('profile',)

    def get_bio(self, instance):
        return instance.profile.bio[:20] + ' ...'
    get_bio.short_description = 'Bio'

    def get_name(self, instance):
        return instance.first_name
    get_name.short_description = 'Name'

    def get_following(self, instance):
        print("instance", instance)
        return instance.following.count()
    get_following.short_description = 'Following'

    def get_followers(self, instance):
        return instance.followers.count()
    get_followers.short_description = 'Followers'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
