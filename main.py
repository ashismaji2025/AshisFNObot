import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
import asyncio

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Env variables
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Flask app
app = Flask(__name__)

# Telegram Bot + Application
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Register command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.process_update(update))
        return "OK", 200
    except Exception as e:
        logger.exception("Error in webhook processing")
        return "Internal Server Error", 500

# Home page
@app.route("/", methods=["GET"])
def home():
    return "AshisF&Obot is live!", 200

# Webhook setup (run only once when hosted)
@app.before_first_request
def set_webhook():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.set_webhook(url=WEBHOOK_URL))
        logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")
    except Exception as e:
        logger.exception("Failed to set webhook")

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
