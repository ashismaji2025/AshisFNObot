import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Load environment variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Shared event loop
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)

# Initialize bot and application
bot = Bot(token=TOKEN)
application = Application.builder().token(TOKEN).build()

# Flask app
app = Flask(__name__)

# Logger (optional but helpful)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

# Add handler to application
application.add_handler(CommandHandler("start", start))

# Webhook receiver route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    event_loop.create_task(application.process_update(update))
    return "OK", 200

# Home route for testing
@app.route("/")
def home():
    return "🤖 AshisF&Obot is running."

# Start everything
if __name__ == "__main__":
    # Set the webhook just once at startup
    async def startup():
        await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook set to: {WEBHOOK_URL}")

    event_loop.run_until_complete(startup())
    app.run(port=10000, host="0.0.0.0")
