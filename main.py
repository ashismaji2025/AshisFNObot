import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Main logic as coroutine
async def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    logger.info("🤖 Bot started with polling")
    await application.run_polling()

# Entry point (no `asyncio.run`, to avoid Render crash)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
