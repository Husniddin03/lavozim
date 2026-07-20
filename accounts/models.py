import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Telefon raqami')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    google_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Google ID')
    telegram_id = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name='Telegram ID')
    role = models.CharField(
        max_length=20,
        choices=[
            ('super_admin', 'Super Admin'),
            ('department_admin', 'Bo\'lim Admin'),
            ('employee', 'Xodim'),
            ('manager', 'Kuzatuvchi'),
            ('mentor', 'Mentor'),
        ],
        default='employee',
        verbose_name='Rol'
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='employees',
        verbose_name='Bo\'lim'
    )
    can_be_mentor = models.BooleanField(default=False, verbose_name='Mentor bo\'la oladimi')

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.get_full_name()} ({self.phone_number})"
