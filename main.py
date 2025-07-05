import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get bot token and webhook URL from environment
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://ashisfnobot.onrender.com/webhook"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Build the app and run webhook
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    run_bot()
