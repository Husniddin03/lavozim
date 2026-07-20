from django.contrib import admin
from .models import RouteDay, ContentBlock, MediaLibrary


class ContentBlockInline(admin.TabularInline):
    model = ContentBlock
    extra = 0
    ordering = ['order_index']


@admin.register(RouteDay)
class RouteDayAdmin(admin.ModelAdmin):
    list_display = ('position', 'day_number', 'title', 'unlock_rule', 'pass_threshold_percent')
    list_filter = ('position', 'unlock_rule')
    inlines = [ContentBlockInline]


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('route_day', 'order_index', 'block_type', 'duration_seconds')
    list_filter = ('block_type',)


@admin.register(MediaLibrary)
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_type', 'uploaded_by', 'tags')
    list_filter = ('file_type',)
