import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

from signals import get_sample_signal  # ✅ Import signal function

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"  # ✅ Safer than exposing full token
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# ✅ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

# ✅ Status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = get_sample_signal()
    await update.message.reply_markdown(signal)

# Add both handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running."

if __name__ == "__main__":
    import asyncio
    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("✅ Webhook set.")
    asyncio.run(run())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
