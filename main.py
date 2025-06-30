import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram.constants import ParseMode
from signals import get_sample_signal

# Get the token and webhook URL
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/{TOKEN}"

# Create Flask and Telegram Application
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisF&Obot is working 💹")

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = get_sample_signal()
    await update.message.reply_text(signal, parse_mode=ParseMode.MARKDOWN)

# Register command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Home page
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running."

# Main runner
if __name__ == "__main__":
    import asyncio
    asyncio.run(application.initialize())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
