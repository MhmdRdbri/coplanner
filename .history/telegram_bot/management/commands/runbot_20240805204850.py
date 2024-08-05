from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.ext import Updater, CommandHandler, Application

import asyncio

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    async def start_bot(self):
        bot_token = 'YOUR_BOT_TOKEN'

        # Initialize the application (updater is a part of it)
        application = Application.builder().token(bot_token).build()

        async def start(update, context):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am a bot!")

        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)

        await application.initialize()
        await application.start_polling()
        await application.updater.start_polling()

        await application.run_until_disconnected()

    def handle(self, *args, **options):
        asyncio.run(self.start_bot())
