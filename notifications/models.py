import uuid
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('daily_reminder', 'Kunlik eslatma'),
        ('streak_warning', 'Streak ogohlantirishi'),
        ('quiz_result', 'Test natijasi'),
        ('recertification_due', 'Qayta o\'qitish eslatmasi'),
        ('mentor_assigned', 'Mentor biriktirildi'),
    ]

    CHANNEL_CHOICES = [
        ('telegram', 'Telegram'),
        ('web_push', 'Web Push'),
        ('email', 'Email'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications', verbose_name='Foydalanuvchi')
    type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES, verbose_name='Turi')
    title = models.CharField(max_length=255, verbose_name='Sarlavha')
    message = models.TextField(verbose_name='Xabar')
    channel = models.CharField(max_length=15, choices=CHANNEL_CHOICES, verbose_name='Kanal')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Yuborilgan sana')
    is_read = models.BooleanField(default=False, verbose_name='O\'qilganmi')

    class Meta:
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'
        ordering = ['-sent_at']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"
