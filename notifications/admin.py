from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'channel', 'sent_at', 'is_read')
    list_filter = ('type', 'channel', 'is_read')
    search_fields = ('user__full_name', 'title')
