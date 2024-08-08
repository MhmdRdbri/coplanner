import logging
from django.core.management.base import BaseCommand
from telegram import Bot
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
            chat_id = user.telegram_chat_id  # Replace with your actual field name
            bot_token = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'  # Replace with your actual bot token

            bot = Bot(token=bot_token)
            bot.send_message(chat_id=chat_id, text=message)
            self.stdout.write(self.style.SUCCESS('Message sent successfully'))

        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR('User not found'))
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))