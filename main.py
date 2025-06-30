import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from signals import get_sample_signal

# Read token from Render environment
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! AshisF&Obot is working 💹")

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = get_sample_signal()
    await update.message.reply_text(signal, parse_mode="Markdown")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Webhook route for Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# Basic home route
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running."

# Set webhook and run Flask
if __name__ == "__main__":
    import asyncio

    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("✅ Webhook set.")
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    asyncio.run(run())
