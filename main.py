import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Read bot token and webhook URL from environment variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
bot = Bot(token=TOKEN)

# Create Flask app
app = Flask(__name__)

# Create Telegram application
application = ApplicationBuilder().token(TOKEN).build()

# === Telegram Bot Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.process_update(update))
        return "OK", 200

# === One-time Webhook Setup ===
@app.before_first_request
def setup_webhook():
    asyncio.run(bot.set_webhook(url=WEBHOOK_URL))
    print("Webhook set to:", WEBHOOK_URL)

# === Run Flask App ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
