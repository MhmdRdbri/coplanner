from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.ext import Application, CommandHandler

import asyncio
import nest_asyncio

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        nest_asyncio.apply()  # Allow the current event loop to be reused
        asyncio.run(self.start_bot())

    async def start_bot(self):
        bot_token = 'YOUR_BOT_TOKEN'

        # Initialize the application
        application = Application.builder().token(bot_token).build()

        async def start(update, context):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am a bot!")

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        await application.initialize()
        await application.run_polling()
