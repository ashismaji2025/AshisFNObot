import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# --- Telegram Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from signals import get_sample_signal
    await update.message.reply_text(get_sample_signal(), parse_mode="Markdown")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# --- Flask Routes ---

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
async def index():
    return "AshisFNObot is running."

# --- Main Section ---
async def main():
    await application.initialize()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    await application.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    asyncio.run(main())
