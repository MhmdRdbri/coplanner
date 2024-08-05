import logging
import os
import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from django.core.management.base import BaseCommand
import nest_asyncio

# Apply nest_asyncio to allow nested use of asyncio
nest_asyncio.apply()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coplanner.settings')
django.setup()

# Get the Django user model
User = get_user_model()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Replace with your actual bot token

# Handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Please send your phone number and password in the format: /login phone_number password')

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text('Please send your phone number and password in the format: /login phone_number password')
        return

    phone_number = args[0]
    password = args[1]

    try:
        user = await sync_to_async(User.objects.get)(phone_number=phone_number)
        if user.check_password(password):
            user.telegram_chat_id = update.message.chat.id
            await sync_to_async(user.save)()
            await update.message.reply_text('Login successful! Your Telegram chat ID has been saved.')
        else:
            await update.message.reply_text('Invalid phone number or password. Please try again.')
    except ObjectDoesNotExist:
        await update.message.reply_text('User not found.')
    except Exception as e:
        await update.message.reply_text('An error occurred: ' + str(e))

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('login', login))

        application.run_polling()

# Ensure this code only runs when executed directly
if __name__ == '__main__':
    Command().handle()
