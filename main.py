import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load token from environment
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/webhook"

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Telegram Application
application = Application.builder().token(TOKEN).build()

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Add /start handler
application.add_handler(CommandHandler("start", start))

# Set webhook and run application
if __name__ == "__main__":
    async def main():
        await application.bot.set_webhook(WEBHOOK_URL)
        logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")
        await application.run_webhook(
            listen="0.0.0.0",
            port=10000,
            webhook_url=WEBHOOK_URL,
        )

    import asyncio
    asyncio.run(main())
