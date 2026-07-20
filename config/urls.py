from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/content/', include('content.urls')),
    path('api/testing/', include('testing.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/mentor/', include('mentor.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('', include('bot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
