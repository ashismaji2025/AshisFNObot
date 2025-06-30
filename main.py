import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram.constants import ParseMode
from signals import get_sample_signal

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/{TOKEN}"

# Flask app
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisF&Obot is working 💹")

# Command: /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = get_sample_signal()
    await update.message.reply_text(signal, parse_mode=ParseMode.MARKDOWN)

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Index route
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is live and listening."

# Startup async runner
async def main():
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(WEBHOOK_URL)

# Launch everything
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
