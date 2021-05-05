from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'get_bio', 'get_name', 'email', 'is_staff')
    list_select_related = ('profile', )

    def get_bio(self, instance):
        return instance.profile.bio[:20] + ' ...'
    get_bio.short_description = 'Bio'

    def get_name(self, instance):
        return instance.first_name
    get_name.short_description = 'Name'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
