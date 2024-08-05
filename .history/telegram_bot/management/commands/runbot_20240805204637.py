from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.ext import Updater, CommandHandler

import asyncio

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    async def start_bot(self):
        bot_token = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'
        bot = Bot(token=bot_token)
        updater = Updater(token=bot_token)
        dispatcher = updater.dispatcher

        def start(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am a bot!")

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        updater.start_polling()
        updater.idle()

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_bot())