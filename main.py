import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Get token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Telegram command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! AshisFNObot is now live 🚀")

# Flask app to keep the service alive
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "AshisFNObot is active!"

# Start the bot
def run():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == '__main__':
    run()