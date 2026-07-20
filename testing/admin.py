from django.contrib import admin
from .models import Question, QuestionOption


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'is_pre_assessment', 'route_day', 'points')
    list_filter = ('question_type', 'is_pre_assessment')
    inlines = [QuestionOptionInline]


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'option_text', 'is_correct')
    list_filter = ('is_correct',)
