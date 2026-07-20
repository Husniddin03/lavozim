import uuid
from django.db import models


class UserPosition(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'Davom etmoqda'),
        ('completed', 'Tugallangan'),
        ('paused', 'To\'xtatilgan'),
        ('not_started', 'Boshlanmagan'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_positions', verbose_name='Foydalanuvchi')
    position = models.ForeignKey('departments.Position', on_delete=models.CASCADE, related_name='user_positions', verbose_name='Lavozim')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Biriktirilgan sana')
    current_day = models.IntegerField(default=0, verbose_name='Hozirgi kun')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='Holat')
    mentor = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='mentored_positions',
        verbose_name='Mentor'
    )
    pre_assessment_score = models.IntegerField(null=True, blank=True, verbose_name='Kirish testi natijasi')
    pre_assessment_passed = models.BooleanField(default=False, verbose_name='Kirish testidan o\'tdimi')
    skipped_days = models.IntegerField(default=0, verbose_name='O\'tkazilgan kunlar')
    certified_at = models.DateTimeField(null=True, blank=True, verbose_name='Sertifikat sanasi')
    certificate_url = models.CharField(max_length=500, blank=True, verbose_name='Sertifikat URL')
    recertification_due = models.DateTimeField(null=True, blank=True, verbose_name='Qayta o\'qitish muddati')
    position_version = models.IntegerField(default=1, verbose_name='Lavozim versiyasi')

    class Meta:
        verbose_name = 'Foydalanuvchi lavozimi'
        verbose_name_plural = 'Foydalanuvchi lavozimlari'
        unique_together = ['user', 'position']

    def __str__(self):
        return f"{self.user} - {self.position}"


class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_position = models.ForeignKey(UserPosition, on_delete=models.CASCADE, related_name='progress', verbose_name='Foydalanuvchi lavozimi')
    route_day = models.ForeignKey('content.RouteDay', on_delete=models.CASCADE, related_name='user_progress', verbose_name='Kun')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tugallangan sana')
    quiz_score_percent = models.IntegerField(null=True, blank=True, verbose_name='Test natijasi (%)')
    attempts_count = models.IntegerField(default=0, verbose_name='Urinishlar soni')
    feedback_rating = models.IntegerField(null=True, blank=True, verbose_name='Baho (1-5)')
    feedback_comment = models.TextField(blank=True, verbose_name='Izoh')
    is_skipped = models.BooleanField(default=False, verbose_name='O\'tkazib yuborilganmi')

    class Meta:
        verbose_name = 'Foydalanuvchi progressi'
        verbose_name_plural = 'Foydalanuvchi progresslari'
        unique_together = ['user_position', 'route_day']

    def __str__(self):
        return f"{self.user_position} - Kun {self.route_day.day_number}"
