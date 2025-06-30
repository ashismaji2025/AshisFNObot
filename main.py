import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BOT_USERNAME = "AshisFNObot"

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis‑da! Your AshisFNObot is active 💹")

telegram_app.add_handler(CommandHandler("start", start))

# Flask route for Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram_app.update_queue.bot._parse_update(request.get_json(force=True))
    telegram_app.create_task(telegram_app.process_update(update))
    return "ok"

# Render expects the Flask app to run
if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"https://ashisfnobot.onrender.com/{TOKEN}"
    )
