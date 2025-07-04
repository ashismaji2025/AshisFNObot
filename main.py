import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Main function to run webhook
async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    logger.info(f"✅ Setting webhook: {WEBHOOK_URL}")
    await application.bot.set_webhook(WEBHOOK_URL)

    await application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
