from django.core.management.base import BaseCommand
from telegram_bot.bot import main

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        main()