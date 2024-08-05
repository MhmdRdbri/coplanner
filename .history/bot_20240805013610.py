import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coplanner.settings')
django.setup()

User = get_user_model()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Please send your phone number and password in the format: /login phone_number password')

def login(update: Update, context: CallbackContext):
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text('Please send your phone number and password in the format: /login phone_number password')
            return
        
        phone_number = args[0]
        password = args[1]
        
        user = authenticate(phone_number=phone_number, password=password)
        
        if user is not None:
            user.telegram_chat_id = update.message.chat_id
            user.save()
            update.message.reply_text('Login successful! Your Telegram chat ID has been saved.')
        else:
            update.message.reply_text('Invalid phone number or password. Please try again.')
    except Exception as e:
        update.message.reply_text('An error occurred: ' + str(e))

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('login', login, pass_args=True))

    updater.start_polling()
    updater.idle()