import logging
import asyncio
from django.core.management.base import BaseCommand
from telegram import Bot
from telegram.error import TelegramError
from account.models import CustomUser  # Replace with your actual user model

class Command(BaseCommand):
    help = 'Send a message to a user via Telegram bot'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='Indicates the user ID')
        parser.add_argument('message', type=str, help='Message to send')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        message = kwargs['message']

        try:
            user = CustomUser.objects.get(id=user_id)
            chat_id = user.telegram_chat_id
            bot_token = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'

            bot = Bot(token=bot_token)

            asyncio.run(self.send_message(bot, chat_id, message))
            self.stdout.write(self.style.SUCCESS('Message sent successfully'))

        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
        except TelegramError as e:
            logging.error(f"Telegram error occurred: {e}")
            self.stdout.write(self.style.ERROR(f"Telegram error occurred: {e}"))
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

    async def send_message(self, bot, chat_id, message):
        try:
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logging.error(f"Failed to send message: {e}")
            raise