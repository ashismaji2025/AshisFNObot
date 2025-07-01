import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

from signals import get_sample_signal

# Create Flask app
app = Flask(__name__)

# Bot token and webhook path
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7526432651:AAE-H5jjoPitEw5WtZ3TxWRg5hhqLZvcnGs")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Build the Telegram app
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Define handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! AshisF&Obot is active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and ready, Ashis-da!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_markdown(get_sample_signal())

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# Flask route to handle Telegram webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook_handler():
    if request.method == "POST":
        await application.update_queue.put(Update.de_json(request.get_json(force=True), application.bot))
        return "OK"
    return "Not allowed", 405

# Setup webhook and run Flask server
if __name__ == "__main__":
    async def set_webhook():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)

    asyncio.run(set_webhook())

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
