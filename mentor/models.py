import uuid
from django.db import models


class MentorNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='mentor_notes', verbose_name='Mentor')
    user_position = models.ForeignKey('progress.UserPosition', on_delete=models.CASCADE, related_name='mentor_notes', verbose_name='Xodim/Lavozim')
    note_text = models.TextField(verbose_name='Izoh')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')

    class Meta:
        verbose_name = 'Mentor izohi'
        verbose_name_plural = 'Mentor izohlari'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.mentor} -> {self.user_position}"
