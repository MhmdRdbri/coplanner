import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

User = get_user_model()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Please send your phone number and password in the format: /login phone_number password')

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text('Please send your phone number and password in the format: /login phone_number password')
            return
        
        phone_number = args[0]
        password = args[1]
        
        user = authenticate(phone_number=phone_number, password=password)
        
        if user is not None:
            user.telegram_chat_id = update.message.chat_id
            user.save()
            await update.message.reply_text('Login successful! Your Telegram chat ID has been saved.')
        else:
            await update.message.reply_text('Invalid phone number or password. Please try again.')
    except Exception as e:
        await update.message.reply_text('An error occurred: ' + str(e))

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('login', login))

    application.run_polling()

if __name__ == '__main__':
    main()
