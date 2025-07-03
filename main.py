import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")  # keep token secure via environment variable

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask and Telegram Application
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()


# Define a simple command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")


# Register handler
application.add_handler(CommandHandler("start", start))


# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.get_event_loop().create_task(application.process_update(update))
    except Exception as e:
        logger.error("Exception in webhook: %s", e)
        return "ERROR", 500
    return "OK", 200


# Root endpoint
@app.route("/")
def index():
    return "AshisFNObot is running 💕"


if __name__ == "__main__":
    print("✅ Webhook set to: https://ashisfnobot.onrender.com/webhook")
    app.run(host="0.0.0.0", port=10000)
