import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/webhook"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram application
application = Application.builder().token(TOKEN).build()

# Define /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I’m alive and ready to serve 💕")

# Add handler
application.add_handler(CommandHandler("start", start))

# Flask route for webhook
@app.post("/webhook")
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
    except Exception as e:
        logger.exception("❌ Error in webhook")
    return "OK", 200

# Set webhook only once at startup
@app.before_first_request
def set_webhook():
    import asyncio
    asyncio.run(application.bot.set_webhook(WEBHOOK_URL))
    logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")

# Run Flask app (Render automatically uses port 10000)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
