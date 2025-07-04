import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get bot token and webhook config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Main runner
async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info(f"✅ Setting webhook to: {WEBHOOK_URL}")
    await application.bot.set_webhook(WEBHOOK_URL)

    await application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
