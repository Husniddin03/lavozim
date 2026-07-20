import uuid
from django.db import models


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Bo\'lim nomi')
    theme_color = models.CharField(max_length=7, default='#3B82F6', verbose_name='Rang (hex)')
    icon_set = models.CharField(max_length=100, default='default', verbose_name='Ikonlar to\'plami')

    class Meta:
        verbose_name = 'Bo\'lim'
        verbose_name_plural = 'Bo\'limlar'

    def __str__(self):
        return self.name


class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions', verbose_name='Bo\'lim')
    name = models.CharField(max_length=255, verbose_name='Lavozim nomi')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    difficulty_level = models.CharField(
        max_length=10,
        choices=[('easy', 'Oson'), ('medium', 'O\'rta'), ('hard', 'Qiyin')],
        default='medium',
        verbose_name='Qiyinlik darajasi'
    )
    total_days = models.IntegerField(default=0, verbose_name='Jami kunlar')
    status = models.CharField(
        max_length=10,
        choices=[('draft', 'Draft'), ('published', 'Published')],
        default='draft',
        verbose_name='Holat'
    )
    recertification_months = models.IntegerField(null=True, blank=True, verbose_name='Qayta o\'qitish (oy)')
    has_pre_assessment = models.BooleanField(default=False, verbose_name='Kirish testi bormi')
    pre_assessment_threshold = models.IntegerField(null=True, blank=True, verbose_name='Kirish testi o\'tish foizi')
    pre_assessment_skip_days = models.IntegerField(null=True, blank=True, verbose_name='O\'tkazib yuboriladigan kunlar')
    version = models.IntegerField(default=1, verbose_name='Versiya')
    effective_from = models.DateTimeField(auto_now_add=True, verbose_name='Kuchga kirish sanasi')

    class Meta:
        verbose_name = 'Lavozim'
        verbose_name_plural = 'Lavozimlar'

    def __str__(self):
        return f"{self.name} ({self.department.name})"
