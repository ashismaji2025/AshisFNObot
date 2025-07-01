import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from signals import get_sample_signal

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Flask App
app = Flask(__name__)

# Telegram App
application = ApplicationBuilder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌟 Welcome to AshisF&Obot! Use /status or /signal to continue.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ AshisF&Obot is active and ready!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal_text = get_sample_signal()
    await update.message.reply_markdown(signal_text)

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# Flask route for webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
async def index():
    return "AshisF&Obot is live 💥"

# Main entry
if __name__ == "__main__":
    import asyncio

    async def run():
        await application.initialize()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        await application.start()
        await application.updater.start_polling()
        await application.updater.idle()

    asyncio.run(run())
