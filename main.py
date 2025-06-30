import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/{TOKEN}"

app = Flask(__name__)

# Async start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

# Main Telegram application setup
async def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Set webhook
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.initialize()
    return application

# Flask route to receive webhook updates
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    bot.update_queue.put_nowait(update)
    return "ok"

# Flask root route
@app.route("/", methods=["GET"])
def home():
    return "AshisFNObot is running 🚀"

# Start both Flask and bot
if __name__ == "__main__":
    bot = asyncio.run(run_bot())  # single event loop start
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
