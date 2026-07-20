from django.contrib import admin
from .models import Department, Position


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme_color')
    search_fields = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'difficulty_level', 'total_days', 'status', 'version')
    list_filter = ('department', 'difficulty_level', 'status')
    search_fields = ('name',)
