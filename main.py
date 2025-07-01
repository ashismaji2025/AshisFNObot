import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from signals import get_sample_signal

# ENV
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"
PORT = int(os.environ.get("PORT", 10000))

# Flask app
app = Flask(__name__)

# Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello Ashis-da! Your AshisFNObot is active!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot status: Fully functional.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_sample_signal(), parse_mode="Markdown")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# --- Webhook route ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running!"

# --- Launch ---
if __name__ == "__main__":
    import os

    async def set_webhook():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)

    import asyncio
    asyncio.run(set_webhook())

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
