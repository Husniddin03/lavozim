from django.core.management.base import BaseCommand
from bot.telegram_bot import run_bot


class Command(BaseCommand):
    help = 'Telegram botni ishga tushiradi'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Telegram bot ishga tushmoqda...'))
        run_bot()
