import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # Example: https://ashisfnobot.onrender.com/webhook

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# Flask route for webhook
@app.post("/webhook")
async def webhook() -> str:
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
    except Exception as e:
        logger.error("Webhook processing failed:", exc_info=e)
        return "ERROR", 500
    return "OK", 200

# Set the webhook on startup
async def set_webhook():
    await application.bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")

# Start bot and Flask app
if __name__ == "__main__":
    import asyncio

    # Set webhook before starting Flask
    asyncio.run(set_webhook())

    # Start Flask
    app.run(port=10000, host="0.0.0.0")
