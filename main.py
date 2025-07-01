import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
from signals import get_sample_signal

# Setup Flask
app = Flask(__name__)

# Bot token and webhook
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7526432651:AAE-H5jjoPitEw5WtZ3TxWRg5hhqLZvcnGs")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Define handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! AshisF&Obot is active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is alive and ready, Ashis-da!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_markdown(get_sample_signal())

# Create application
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# Flask route to handle Telegram webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.create_task(application.process_update(update))
    return "OK", 200

# Set webhook and run server
async def run():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set to", WEBHOOK_URL)
    await application.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    asyncio.run(run())
