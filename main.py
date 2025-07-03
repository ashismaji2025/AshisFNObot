import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Load env vars
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Create Flask app
app = Flask(__name__)

# Create Telegram Application (not initialized yet)
application = ApplicationBuilder().token(TOKEN).build()

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# Define /webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    # Use asyncio.run to safely run inside Flask thread
    async def process():
        await application.initialize()
        await application.process_update(update)

    asyncio.run(process())
    return "OK", 200

# Root route (health check)
@app.route("/")
def home():
    return "✅ AshisFNObot is live", 200

# Set webhook before first request
@app.before_first_request
def setup():
    async def set_webhook():
        await application.bot.set_webhook(WEBHOOK_URL)
    asyncio.run(set_webhook())
    print("✅ Webhook set to:", WEBHOOK_URL)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
