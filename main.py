import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from signals import get_sample_signal

TOKEN = TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = f"/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

application = ApplicationBuilder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AshisFNObot is active 💹")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: Operational ✅")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_sample_signal())

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# Flask setup
app = Flask(__name__)

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))  # ✅ Use run, not create_task
        return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is alive 🔥"

if __name__ == "__main__":
    async def setup():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        await application.start()

    PORT = int(os.environ.get("PORT", 5000))  # fallback to 5000
app.run(host="0.0.0.0", port=PORT)
