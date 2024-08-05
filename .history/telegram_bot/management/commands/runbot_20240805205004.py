from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.ext import Application, CommandHandler

import asyncio

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    async def start_bot(self):
        bot_token = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'

        # Initialize the application (updater is a part of it)
        application = Application.builder().token(bot_token).build()

        async def start(update, context):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am a bot!")

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        await application.initialize()
        
        # Start polling
        await application.run_polling()

    def handle(self, *args, **options):
        asyncio.run(self.start_bot())
