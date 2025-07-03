import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Flask app
app = Flask(__name__)

# Telegram bot and application
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Telegram Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        # Handle update using PTB async function safely
        application.update_queue.put_nowait(update)
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "Internal Server Error", 500

# Startup Webhook Setup
@app.before_request
def init():
    if not hasattr(app, 'webhook_set'):
        app.webhook_set = True
        import asyncio
        asyncio.get_event_loop().run_until_complete(bot.set_webhook(url=WEBHOOK_URL))
        logger.info(f"Webhook set to: {WEBHOOK_URL}")
    logger.info("Setting webhook...")
    import asyncio
    asyncio.get_event_loop().run_until_complete(bot.set_webhook(url=WEBHOOK_URL))
    logger.info(f"Webhook set to: {WEBHOOK_URL}")

# Flask Server
if __name__ == "__main__":
    application.run_polling()  # Needed to start background async workers
    app.run(port=10000, host="0.0.0.0")
