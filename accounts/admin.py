from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'role', 'department', 'can_be_mentor')
    list_filter = ('role', 'department', 'can_be_mentor')
    search_fields = ('phone_number', 'full_name', 'username')
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('phone_number', 'role', 'department', 'can_be_mentor', 'telegram_id', 'google_id')}),
    )
