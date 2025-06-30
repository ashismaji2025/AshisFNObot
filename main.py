import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from signals import get_sample_signal
import asyncio

# Telegram bot token from environment
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"
PORT = int(os.environ.get("PORT", 10000))

# Initialize Flask
app = Flask(__name__)

# Initialize Telegram bot application
application = ApplicationBuilder().token(TOKEN).build()

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is active 💹")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot status: Working fine.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_sample_signal(), parse_mode="Markdown")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# Webhook endpoint (called by Telegram server)
@app.route(WEBHOOK_PATH, methods=["POST"])
def receive_update():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Optional root endpoint
@app.route("/")
def home():
    return "AshisFNObot is alive."

# Startup logic with webhook setup
if __name__ == "__main__":
    async def main():
        await application.initialize()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        await application.start()
        await application.updater.start_polling()
        await application.updater.idle()

    asyncio.run(main())
