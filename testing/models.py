import uuid
from django.db import models


class Question(models.Model):
    QUESTION_TYPES = [
        ('single_choice', 'Bir tanlovli'),
        ('multi_choice', 'Ko\'p tanlovli'),
        ('scenario_choice', 'Stsenariy'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route_day = models.ForeignKey(
        'content.RouteDay',
        on_delete=models.CASCADE,
        related_name='questions',
        null=True, blank=True,
        verbose_name='Kun'
    )
    is_pre_assessment = models.BooleanField(default=False, verbose_name='Kirish testi savolimi')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name='Savol turi')
    question_text = models.TextField(verbose_name='Savol matni')
    media_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='Media URL')
    explanation_text = models.TextField(blank=True, verbose_name='Tushuntirish')
    points = models.IntegerField(default=1, verbose_name='Ball')
    version = models.IntegerField(default=1, verbose_name='Versiya')

    class Meta:
        verbose_name = 'Savol'
        verbose_name_plural = 'Savollar'

    def __str__(self):
        return self.question_text[:80]


class QuestionOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name='Savol')
    option_text = models.CharField(max_length=500, verbose_name='Javob varianti')
    is_correct = models.BooleanField(default=False, verbose_name='To\'g\'rimi')

    class Meta:
        verbose_name = 'Javob varianti'
        verbose_name_plural = 'Javob variantlari'

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} {self.option_text}"
