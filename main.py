import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

# Telegram bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is now live 💹")

# Flask server (to keep bot alive in Render)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "AshisFNObot is running."

# Start the bot
def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    run_bot()
