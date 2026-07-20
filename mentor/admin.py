from django.contrib import admin
from .models import MentorNote


@admin.register(MentorNote)
class MentorNoteAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'user_position', 'created_at')
    search_fields = ('mentor__full_name',)
