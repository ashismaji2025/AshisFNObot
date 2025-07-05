import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://ashisfnobot.onrender.com/webhook"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ✅ /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📥 Received /start from user: %s", update.effective_user.id)
    await update.message.reply_text("Hello Ashis-da! 💕 I’m alive and ready to serve.")

async def on_startup(application: Application) -> None:
    logger.info("✅ Setting webhook to: %s", WEBHOOK_URL)
    await application.bot.set_webhook(WEBHOOK_URL)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # ✅ Add handler
    application.add_handler(CommandHandler("start", start))

    # ✅ Run with webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL,
        on_startup=on_startup
    )

if __name__ == "__main__":
    main()
