import uuid
from django.db import models


class RouteDay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.ForeignKey('departments.Position', on_delete=models.CASCADE, related_name='route_days', verbose_name='Lavozim')
    day_number = models.IntegerField(verbose_name='Kun raqami')
    title = models.CharField(max_length=255, verbose_name='Kun sarlavhasi')
    node_image_url = models.CharField(max_length=500, blank=True, verbose_name='Tugun rasmi')
    unlock_rule = models.CharField(
        max_length=20,
        choices=[
            ('previous_completed', 'Oldingi kun tugallansa'),
            ('date_based', 'Ma\'lum sanada ochiladi'),
            ('manual', 'Admin qo\'lda ochadi'),
        ],
        default='previous_completed',
        verbose_name='Ochilish qoidasi'
    )
    pass_threshold_percent = models.IntegerField(default=80, verbose_name='O\'tish foizi')
    is_skippable = models.BooleanField(default=False, verbose_name='O\'tkazib yuborish mumkinmi')
    version = models.IntegerField(default=1, verbose_name='Versiya')

    class Meta:
        verbose_name = 'Route Map kuni'
        verbose_name_plural = 'Route Map kunlari'
        ordering = ['day_number']
        unique_together = ['position', 'day_number']

    def __str__(self):
        return f"{self.position.name} - Kun {self.day_number}: {self.title}"


class ContentBlock(models.Model):
    BLOCK_TYPES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Matn'),
        ('image_text', 'Rasm + Matn'),
        ('scenario', 'Stsenariy'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route_day = models.ForeignKey(RouteDay, on_delete=models.CASCADE, related_name='content_blocks', verbose_name='Kun')
    order_index = models.IntegerField(verbose_name='Tartib')
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES, verbose_name='Blok turi')
    media_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='Media URL')
    text_content = models.TextField(blank=True, null=True, verbose_name='Matn')
    duration_seconds = models.IntegerField(null=True, blank=True, verbose_name='Davomiylik (soniya)')
    version = models.IntegerField(default=1, verbose_name='Versiya')

    class Meta:
        verbose_name = 'Kontent blok'
        verbose_name_plural = 'Kontent bloklar'
        ordering = ['order_index']

    def __str__(self):
        return f"{self.route_day} - Blok {self.order_index}: {self.get_block_type_display()}"


class MediaLibrary(models.Model):
    FILE_TYPES = [
        ('image', 'Rasm'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='media_library/', verbose_name='Fayl')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, verbose_name='Fayl turi')
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, verbose_name='Yuklagan')
    tags = models.TextField(blank=True, verbose_name='Teglar')

    class Meta:
        verbose_name = 'Media kutubxona'
        verbose_name_plural = 'Media kutubxona'

    def __str__(self):
        return f"{self.file.name} ({self.get_file_type_display()})"
