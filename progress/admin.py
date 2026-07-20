from django.contrib import admin
from .models import UserPosition, UserProgress


@admin.register(UserPosition)
class UserPositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'current_day', 'status', 'mentor', 'pre_assessment_passed')
    list_filter = ('status', 'position', 'pre_assessment_passed')
    search_fields = ('user__phone_number', 'user__full_name')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user_position', 'route_day', 'quiz_score_percent', 'attempts_count', 'is_skipped')
    list_filter = ('is_skipped',)
