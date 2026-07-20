from django.contrib import admin
from .models import UserGamification


@admin.register(UserGamification)
class UserGamificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'xp_total', 'current_streak', 'longest_streak', 'level')
    search_fields = ('user__phone_number', 'user__full_name')
