import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load bot token and webhook info
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Main function to start webhook
async def main():
    application = Application.builder().token(TOKEN).build()

    # Add your handlers
    application.add_handler(CommandHandler("start", start))

    # Set the Telegram webhook
    await application.bot.set_webhook(WEBHOOK_URL)

    # Start the webhook server (native PTB server)
    await application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
