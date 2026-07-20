import uuid
from django.db import models


class UserGamification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='gamification', verbose_name='Foydalanuvchi')
    xp_total = models.IntegerField(default=0, verbose_name='Jami XP')
    current_streak = models.IntegerField(default=0, verbose_name='Hozirgi streak')
    longest_streak = models.IntegerField(default=0, verbose_name='Eng uzun streak')
    level = models.IntegerField(default=1, verbose_name='Daraja')
    last_activity_date = models.DateField(null=True, blank=True, verbose_name='Oxirgi faoliyat')

    class Meta:
        verbose_name = 'O\'yin ko\'rsatkichi'
        verbose_name_plural = 'O\'yin ko\'rsatkichlari'

    def __str__(self):
        return f"{self.user} - XP: {self.xp_total}, Level: {self.level}"
