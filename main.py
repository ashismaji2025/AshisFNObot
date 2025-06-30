import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from flask import Flask, request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = "https://ashisfnobot.onrender.com"

app_flask = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis‑da! Your AshisFNObot is active 💹")

telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))

@app_flask.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "ok"

@app_flask.route("/", methods=["GET"])
async def set_webhook():
    await telegram_app.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    return "Webhook set"

if __name__ == "__main__":
    import asyncio
    asyncio.run(telegram_app.initialize())
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
