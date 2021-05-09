from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import debug_toolbar

urlpatterns = [
    # Debug toolbar
    path('__debug__/', include(debug_toolbar.urls)),

    # Django Admin
    path('admin/', admin.site.urls),

    # User profiles
    path('my/', include('profiles.urls')),

    # User management
    path('accounts/', include('allauth.urls')),

    # notifications
    path('', include('actions.urls')),
    # Pages app
    path('', include('pages.urls')),

]

if settings.DEBUG:
    # For serving media files in development
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
